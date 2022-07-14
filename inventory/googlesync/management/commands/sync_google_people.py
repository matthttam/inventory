from googlesync.exceptions import SyncProfileNotFound

from googlesync.models import (
    GooglePersonMapping,
    GooglePersonTranslation,
    GooglePersonSyncProfile,
    GoogleSyncProfileAbstract,
)

from django.core.exceptions import ValidationError
from django.db.models import Q
from django.db import transaction

from ._google_sync import GoogleSyncCommand
from people.models import Person, PersonStatus


class Command(GoogleSyncCommand):
    help = "Syncs google users to inventory people."

    def add_arguments(self, parser):
        parser.add_argument("profiles", nargs="+", help="list each profile to sync")

    def handle(self, *args, **options):
        profile_names = options.get("profiles")

        # Get each sync profile based on profile names passed
        self.sync_profiles = []
        for profile_name in profile_names:
            self.sync_profiles.append(self._get_person_sync_profile(profile_name))

        # Loop over each sync profile and sync people
        for sync_profile in self.sync_profiles:
            self.stdout.write(
                self.style.NOTICE(f"Starting people sync: {sync_profile.name}")
            )
            self.sync_google_people(sync_profile)

        self.stdout.write(self.style.SUCCESS("Done"))

    def _get_person_sync_profile(self, profile_name):
        try:
            sync_profile = GooglePersonSyncProfile.objects.get(name=profile_name)
        except GooglePersonSyncProfile.DoesNotExist:
            raise SyncProfileNotFound(profile_name=profile_name)
        return sync_profile

    def _get_google_records(self, query) -> list:
        users = self._get_users_service()

        request = users.list(
            domain=self.customer.get("customerDomain"),
            projection="full",
            query=query,
        )
        google_user_records = []
        while request is not None:
            response = request.execute()
            google_users = response.get("users")
            if not google_users:
                self.stdout.write(
                    self.style.WARNING(f"No users found with google query: {query!r}")
                )
                return None

            google_user_records.extend(google_users)
            request = users.list_next(request, response)
            # request = None
        return google_user_records

    def sync_google_people(self, sync_profile):
        google_users = self._get_google_records(query=sync_profile.google_query)
        person_records = self.convert_google_users_to_person(sync_profile, google_users)
        print(f"Number of person records: {len(person_records)}")

        self.stdout.write(
            self.style.SUCCESS(f"Total Number of person records: {len(person_records)}")
        )
        # active_person_status = PersonStatus.objects.filter(is_inactive=False).first()
        inactive_person_status = PersonStatus.objects.filter(is_inactive=True).first()
        found_record_ids = []
        records_to_update = []
        records_to_create = []
        records_to_skip = []
        for person_record in person_records:

            # Use lookup ids in order of matching_priority
            lookup_ids = [
                x.to_field
                for x in sync_profile.mappings.exclude(matching_priority=None).order_by(
                    "matching_priority"
                )
            ]

            # Build a query to search through each ID specified
            query = Q()
            for id_field in lookup_ids:
                query.add(Q(**{id_field: getattr(person_record, id_field)}), Q.OR)
            id = getattr(Person.objects.filter(query).first(), "id", None)
            if id:
                found_record_ids.append(id)
                person_record.id = id
                records_to_update.append(person_record)
            else:
                if person_record.status == inactive_person_status:
                    records_to_skip.append(person_record)
                else:
                    records_to_create.append(person_record)

        print(f"Number of person records to update: {len(records_to_update)}")
        print(f"Number of person records to create: {len(records_to_create)}")
        print(f"Number of person records to skip: {len(records_to_skip)}")

        # Update found records
        if records_to_update:
            excluded_fields = ["id"]
            fields = [
                x.name for x in Person._meta.fields if (x.name not in excluded_fields)
            ]
            Person.objects.bulk_update(records_to_update, fields=fields)

            # Inactivate Records Not Found
            missing_records = (
                Person.objects.exclude(google_id__isnull=True)
                .filter(type=sync_profile.person_type)
                .difference(Person.objects.filter(id__in=found_record_ids))
            )

            with transaction.atomic():
                for missing_record in missing_records:
                    missing_record.status = inactive_person_status
                    missing_record.save()
                    self.stdout.write(
                        self.style.WARNING(
                            f"Person not found. Setting to Inactive: {missing_record}"
                        )
                    )

        # Create New Records
        if records_to_create:
            Person.objects.bulk_create(records_to_create)

    def convert_google_users_to_person(
        self, sync_profile: GooglePersonSyncProfile, google_users: list
    ) -> list[Person]:
        person_records = []
        for google_user in google_users:
            person = self.convert_google_user_to_person(sync_profile, google_user)
            if not person:
                continue
            person_records.append(person)
        return person_records

    def convert_google_user_to_person(
        self, sync_profile: GooglePersonSyncProfile, google_user: dict
    ) -> Person:

        person_dictionary = self._map_dictionary(sync_profile, google_user)
        person_dictionary["type"] = sync_profile.person_type
        person_dictionary["status"] = PersonStatus.objects.filter(
            name=person_dictionary["status"]
        ).first()
        buildings = person_dictionary.pop("buildings", None)
        rooms = person_dictionary.pop("rooms", None)
        person = Person(**person_dictionary)
        person._buildings = buildings or None
        person._rooms = rooms or None

        try:

            person.clean_fields()
        except ValidationError as e:
            self.stdout.write(
                self.style.WARNING(
                    f"Failed to convert google user data to person: {person_dictionary}"
                )
            )
            self.stdout.write(self.style.WARNING(f"{e.message_dict}"))
            return None
        return person