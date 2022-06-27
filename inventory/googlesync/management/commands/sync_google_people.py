from django.core.management.base import BaseCommand, CommandError
from googlesync.exceptions import ConfigNotFound, SyncProfileNotFound, GoogleQueryEmptyResultSet
from googlesync.models import (
    GooglePersonMapping,
    GooglePersonTranslation,
    GooglePersonSyncProfile,
)
from people.models import Person, PersonStatus
from django.core.exceptions import ValidationError
import googleapiclient.discovery

# from googlesync.models import *

from ._google_sync import GoogleSyncCommand
from django.db.models import Q
from django.db import transaction

class Command(GoogleSyncCommand):
    help = "Syncs google users to inventory people."

    def add_arguments(self, parser):
        parser.add_argument("profiles", nargs="+")

    def handle(self, *args, **options):

        # Verify service account google config exists
        google_config = self._get_google_config()
        if not google_config:
            self.stdout.write(self.style.ERROR("Failed to find google sync config!"))
            raise ConfigNotFound(config_name="Google Sync")

        # Get Google credentials
        credentials = self._get_google_credentials(google_config)

        # Parse command
        profiles = options.get("profiles")

        for profile in profiles:
            self.sync_google_people(credentials, profile)
        self.stdout.write(self.style.SUCCESS("Working!"))

    def sync_google_people(self, credentials, profile_name):
        self.stdout.write(self.style.NOTICE(f"Starting people sync: {profile_name}"))

        try:
            sync_profile = GooglePersonSyncProfile.objects.get(name=profile_name)
        except GooglePersonSyncProfile.DoesNotExist:
            raise SyncProfileNotFound(profile_name=profile_name)

        service = googleapiclient.discovery.build(
            "admin", "directory_v1", credentials=credentials
        )

        users = service.users()
        person_records = []
        request = users.list(
            domain=self.TARGET, projection="full", query=sync_profile.google_query
        )
        while request is not None:
            response = request.execute()
            if not response.get('users'):
                self.stdout.write(self.style.WARNING(f"No users found with google query: {sync_profile.google_query!r}"))
                return None
            #try:
                
            #    if response.status_code != 200:
                    #if response.reason
            #        raise ValueError
            #except ValueError:
            #    print('error')

            for user in response.get("users"):
                google_person = self.convert_user_to_person(sync_profile, user)
                google_person["type"] = sync_profile.person_type
                google_person['status'] = PersonStatus.objects.filter(name=google_person['status']).first()

                #print(google_person)
                person = Person(**google_person)
                try:
                    person.clean_fields()
                except ValidationError as e:
                    self.stdout.write(self.style.WARNING(f"Validation Error when validating google user: {google_person}"))
                    self.stdout.write(self.style.WARNING(f"{e.message_dict}"))
                    continue
                #obj, created = Person.objects.update_or_create(
                #   defaults=google_person, google_id=google_person['google_id']
                #)
                person_records.append(person)
            request = users.list_next(request, response)
            #request = None
        print(f"Number of person records: {len(person_records)}")

        #active_person_status = PersonStatus.objects.filter(name='Active').first()
        inactive_person_status = PersonStatus.objects.filter(name='Inactive').first()
        found_record_ids = []
        records_to_update = []
        records_to_create = []
        records_to_skip = []
        for person_record in person_records:

            # Build a query to search through each ID specified
            query = Q()
            
            # Use lookup ids in order of matching_priority
            lookup_ids = [x.person_field for x in GooglePersonMapping.objects.exclude(matching_priority = None).order_by('matching_priority')]
            for id_field in lookup_ids:
                query.add(Q(**{id_field: getattr(person_record, id_field)}), Q.OR)
            id = getattr(Person.objects.filter(query).first(), 'id', None)
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
            excluded_fields = ['id']
            fields = [x.name for x in Person._meta.fields if (x.name not in excluded_fields)]
            Person.objects.bulk_update(records_to_update, fields=fields)
        
        # Inactivate Records Not Found
            missing_records = Person.objects.exclude(google_id__isnull=True).filter(type=sync_profile.person_type).difference(Person.objects.filter(id__in=found_record_ids))
            
            with transaction.atomic():
                for missing_record in missing_records:
                    missing_record.status=inactive_person_status
                    missing_record.save()
                    self.stdout.write(self.style.WARNING(f"Person not found. Setting to Inactive: {missing_record}"))
                    #Person.objects.update(, fields=)


        # Create New Records
        if records_to_create:
            Person.objects.bulk_create(records_to_create)

        
    def convert_user_to_person(self, sync_profile: GooglePersonSyncProfile, user: dict) -> dict:
        
        person = {}

        mappings = GooglePersonMapping.objects.filter(
            google_person_sync_profile = sync_profile
        )
        
        

        for mapping in mappings:
            try:
                person[mapping.person_field] = self._extract_from_dictionary(
                    user, mapping.google_field.split(".")
                )
            except KeyError:
                person[mapping.person_field] = None

            # Use translations to convert one value to another
            translations = GooglePersonTranslation.objects.filter(
                google_person_mapping = mapping
            )
        
            for translation in translations:
                if str(person[mapping.person_field]) == translation.translate_from:
                    person[mapping.person_field] = translation.translate_to

        return person

        # while response.
        # print(response)
        # print(type(response['users'][3]))
        # print(response['users'][3])
        # response = service.schemas().list(customerId="C00ys3lij").execute()
        # print(response)

        # google_id = "id"
        # person_type = Mapping_person_type
        # Status False = Active

    # Helper function to drill down into a dictionary based on keys
