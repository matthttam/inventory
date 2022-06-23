from inspect import Attribute
from django.core.management.base import BaseCommand, CommandError
from googlesync.exceptions import ConfigNotFound
from googlesync.models import GoogleServiceAccountConfig
from django.forms import model_to_dict
# pip install --upgrade google-api-python-client google-auth google-auth-httplib2
from google.oauth2 import service_account
import googleapiclient.discovery
from googlesync.models import *
import json


class Command(BaseCommand):
    help = "Syncs google users"

    def add_arguments(self, parser):
        parser.add_argument('system', type=str, nargs='?', default='all')

    def handle(self, *args, **options):
        self.google_config = self.get_google_config()
        if not self.google_config:
            self.stdout.write(self.style.ERROR(
                "Failed to find google sync config!"))
            raise ConfigNotFound(config_name="Google Sync")

        system = options.get('system')
        match system:
            case "all":
                self.sync_google_people()
            case "people":
                self.sync_google_people()
            case _:
                self.stdout.write(self.style.ERROR(
                    f"Unknown system: {system!r}."))
        self.stdout.write(self.style.SUCCESS("Working!"))

    def get_google_config(self):
        try:
            return model_to_dict(GoogleServiceAccountConfig.objects.first())
        except AttributeError:
            return None

    def sync_google_people(self):
        self.stdout.write(self.style.NOTICE("Starting people sync"))

        SCOPES = ['https://www.googleapis.com/auth/admin.directory.user.readonly']
        # Service account will impersonate this user. Must have proper admin privileges in G Suite.
        DELEGATE = 'matt.henry.admin@owensboro.kyschools.us'
        # Service account wants to access data from this.
        TARGET = 'owensboro.kyschools.us'
        service_account_info = json.loads(json.dumps(
            model_to_dict(GoogleServiceAccountConfig.objects.first())))
        credentials = service_account.Credentials.from_service_account_info(
            service_account_info, scopes=SCOPES)
        credentials_delegated = credentials.with_subject(DELEGATE)

        service = googleapiclient.discovery.build(
            'admin', 'directory_v1', credentials=credentials_delegated)
        response = service.users().list(domain=TARGET).execute()

        print(response['users'][0])
