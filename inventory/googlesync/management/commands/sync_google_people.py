from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Q
from googlesync.exceptions import SyncProfileNotFound
from googlesync.models import (
    GoogleCustomSchema,
    GoogleCustomSchemaField,
    GooglePersonSyncProfile,
)
from people.models import Person, PersonStatus

from ._google_sync import GoogleSyncCommandAbstract


class Command(GoogleSyncCommandAbstract):
    help = "Syncs google users to inventory people."

    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(
            title="Command Options", help="", dest="command"
        )
        ### init command ###
        init_subparser = subparsers.add_parser(
            "init",
            help="Initialize google person sync by pulling user schema data from google.",
        )
        init_subparser.add_argument(
            "--force",
            action="store_true",
            help="Used to reinitialize the google user schema. Do this if new custom fields have been added to Google.",
        )
        ### profiles command ###
        sync_subparser = subparsers.add_parser(
            "sync", help="Used to initiate a sync of all profiles."
        )
        sync_subparser.add_argument(
            "profiles", nargs="*", help="List of user profiles to sync."
        )

    def handle(self, *args, **options):
        command = options.get("command")
        if command == "init":
            force = options.get("force")
            self._initialize_person_sync(force=force)
        elif command == "sync":
            profile_names = options.get("profiles")
            # Get each sync profile based on profile names passed
            self.sync_profiles = []
            for profile_name in profile_names:
                self.sync_profiles.append(self._get_person_sync_profile(profile_name))
            self._sync_google_profiles(self.sync_profiles)
        else:
            return False

        self.stdout.write(self.style.SUCCESS("Done"))

    def _sync_google_profiles(self, sync_profiles: list[GooglePersonSyncProfile]):
        for sync_profile in sync_profiles:
            self._sync_google_profile(sync_profile)

    def _sync_google_profile(self, sync_profile: GooglePersonSyncProfile):
        self.stdout.write(
            self.style.SUCCESS(f"Starting people sync: {sync_profile.name!r}")
        )
        self.sync_google_people(sync_profile)

    @transaction.atomic
    def _initialize_person_sync(self, force):
        """Gets all schema information and saves it to the database."""
        self.stdout.write(self.style.SUCCESS(f"Starting people sync initialization."))
        if self.google_config.get("person_initialized"):
            if not force:
                self.stdout.write(
                    self.style.ERROR(
                        f"Google Person Sync already initialized. Use --force to override."
                    )
                )
                return
            else:
                self.stdout.write(self.style.WARNING(f"Forcing reinitialization."))
        self._initialize_person_sync_custom_schemas()
        self._initialize_person_sync_default_schema()

        # Set acocunt as initialized
        google_config = self._get_google_config()
        google_config.person_initialized = True
        google_config.save()

    def _initialize_person_sync_custom_schemas(self):
        schemas = self._get_schemas_service()
        request = schemas.list(customerId=self.customer.get("id"))
        response = request.execute()
        google_schemas = response.get("schemas")
        # Delete any schemas already stored
        GoogleCustomSchema.objects.all().delete()
        # Populate custom chema data
        for gs in google_schemas:
            current_schema = GoogleCustomSchema.objects.create(
                service_account_config_id=self.google_config.get("id"),
                schema_id=gs.get("schemaId"),
                schema_name=gs.get("schemaName"),
                display_name=gs.get("displayName"),
                kind=gs.get("kind"),
                etag=gs.get("etag"),
            )

            for f in gs.get("fields"):
                GoogleCustomSchemaField.objects.create(
                    schema=current_schema,
                    field_name=f.get("fieldName"),
                    field_id=f.get("fieldId"),
                    field_type=f.get("fieldType"),
                    multi_valued=f.get("multiValued", False),
                    kind=f.get("kind"),
                    etag=f.get("etag"),
                    indexed=f.get("indexed", False),
                    display_name=f.get("displayName"),
                    read_access_type=f.get("readAccessType"),
                    numeric_indexing_spec_min_value=f.get(
                        "numericIndexingSpec", {}
                    ).get("minValue", None),
                    numeric_indexing_spec_max_value=f.get(
                        "numericIndexingSpec", {}
                    ).get("maxValue", None),
                )

    def _initialize_person_sync_default_schema(self):
        users = self._get_users_service()
        user_schema = users._schema.get("User")
        print(type(user_schema.get("properties")))
        for etag, property in user_schema.get("properties").items():
            print(f"{etag}: {property}")
            return

    def _get_person_sync_profile(self, profile_name):
        try:
            sync_profile = GooglePersonSyncProfile.objects.get(name=profile_name)
        except GooglePersonSyncProfile.DoesNotExist:
            raise SyncProfileNotFound(profile_name=profile_name)
        return sync_profile

    def _get_google_records(self, query, domain) -> list:
        users = self._get_users_service()
        options = {
            "projection": "full",
            "query": query,
        }
        if domain == "":
            options["customer"] = self.customer.get("id")
        else:
            options["domain"] = domain
        request = users.list(**options)
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

        return google_user_records

    def sync_google_people(self, sync_profile):
        google_users = self._get_google_records(
            query=sync_profile.google_query, domain=sync_profile.domain
        )
        person_records = self.convert_google_users_to_person(sync_profile, google_users)

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

        self.stdout.write(
            self.style.SUCCESS(
                (f"Number of person records to update: {len(records_to_update)}")
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                (f"Number of person records to create: {len(records_to_create)}")
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                (f"Number of person records to skip: {len(records_to_skip)}")
            )
        )

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
