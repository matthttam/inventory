from inspect import Attribute
from django.core.management.base import BaseCommand, CommandError
from googlesync.exceptions import ConfigNotFound
from googlesync.models import GoogleServiceAccountConfig, GooglePersonMapping
from people.models import Person
from django.forms import model_to_dict
from django.db import transaction

from google.oauth2 import service_account
import googleapiclient.discovery
from googlesync.models import *
import json


class Command(BaseCommand):
    help = "Syncs google users"

    def add_arguments(self, parser):
        parser.add_argument('system', type=str, nargs='?', default='all')

    def handle(self, *args, **options):
        # Verify service account google config exists
        google_config = self.get_google_config()
        if not google_config:
            self.stdout.write(self.style.ERROR(
                "Failed to find google sync config!"))
            raise ConfigNotFound(config_name="Google Sync")

        # Build credentials
        credentials = self.get_google_credentials(google_config)

        # Parse command
        system = options.get('system')
        match system:
            case "all":
                self.sync_google_people(credentials)
            case "people":
                self.sync_google_people(credentials)
            case _:
                self.stdout.write(self.style.ERROR(
                    f"Unknown system: {system!r}."))
        self.stdout.write(self.style.SUCCESS("Working!"))

    def get_google_config(self):
        try:
            return model_to_dict(GoogleServiceAccountConfig.objects.first())
        except AttributeError:
            return None

    def get_google_credentials(self, config):
        SCOPES = ['https://www.googleapis.com/auth/admin.directory.user.readonly']

        # Service account wants to access data from this.
        #config = model_to_dict(GoogleServiceAccountConfig.objects.first())
        self.TARGET = config.pop('target')
        self.DELEGATE = config.pop('delegate')

        # Parse the config into a json string and load it into a json object
        service_account_info = json.loads(json.dumps(config))
        credentials = service_account.Credentials.from_service_account_info(
            service_account_info, scopes=SCOPES)
        credentials_delegated = credentials.with_subject(self.DELEGATE)

        return credentials_delegated

    def sync_google_people(self, Credentials):
        self.stdout.write(self.style.NOTICE("Starting people sync"))
        service = googleapiclient.discovery.build(
            'admin', 'directory_v1', credentials=Credentials)
        query = "orgUnitPath=/Staff"
        #query = "givenName=Matt"
        # Get Mappings

        users = service.users()
        request = users.list(domain=self.TARGET, projection="full",
                             query=query)
        while request is not None:
            response = request.execute()
            for user in response['users']:
                google_person = self.convert_user_to_person(user)
                print(google_person)
                obj, created = Person.objects.update_or_create(
                    defaults=google_person, google_id=google_person['google_id']
                )
                #
            #request = users.list_next(request, response)

    def convert_user_to_person(self, user: dict) -> dict:
        mappings = GooglePersonMapping.objects.all()
        person = {}

        for mapping in mappings:
            person[mapping.person_field] = self.extract_from_dictionary(
                user, mapping.google_field.split('.'))
        return person

        # while response.
        # print(response)
        # print(type(response['users'][3]))
        # print(response['users'][3])
        #response = service.schemas().list(customerId="C00ys3lij").execute()
        # print(response)

        # google_id = "id"
        # person_type = Mapping_person_type
        # Status False = Active

    # Helper function to drill down into a dictionary based on keys

    def extract_from_dictionary(self, dictionary: dict, keys: list):
        value = dictionary
        for key in keys:
            value = value[key]
        return value
