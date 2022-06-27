from django.core.management.base import BaseCommand, CommandError

from google.oauth2 import service_account
import json

from django.forms import model_to_dict
from googlesync.models import GoogleServiceAccountConfig

class GoogleSyncCommand(BaseCommand):
    
    def _get_google_config(self):
        try:
            return model_to_dict(GoogleServiceAccountConfig.objects.first())
        except AttributeError:
            return None

    def _get_google_credentials(self, config):
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
    
    def _extract_from_dictionary(self, dictionary: dict, keys: list):
        value = dictionary
        for key in keys:
            value = value[key]
        return value