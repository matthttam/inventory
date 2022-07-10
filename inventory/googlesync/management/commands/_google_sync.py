from django.core.management.base import BaseCommand, CommandError

from google.oauth2 import service_account
import googleapiclient.discovery
import json

from django.forms import model_to_dict
from googlesync.models import GoogleServiceAccountConfig
from googlesync.exceptions import ConfigNotFound


class GoogleSyncCommand(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Get the google config
        self.google_config = self._get_google_config()
        self.DELEGATE = self.google_config.pop("delegate")

        # Retreive current customer information used by other services
        self.customer = self._get_my_customer()

    def _get_google_config(self) -> dict:
        try:
            google_config = model_to_dict(GoogleServiceAccountConfig.objects.first())
        except AttributeError:
            self.stdout.write(self.style.ERROR("Failed to find google sync config!"))
            raise ConfigNotFound(config_name="Google Sync")

        return google_config

    def _get_google_credentials(self, scopes: list):
        # Parse the config into a json string and load it into a json object
        credentials = service_account.Credentials.from_service_account_info(
            json.loads(json.dumps(self.google_config)), scopes=scopes
        )
        credentials_delegated = credentials.with_subject(self.DELEGATE)
        return credentials_delegated

    def _get_my_customer(self):

        service = googleapiclient.discovery.build(
            "admin",
            "directory_v1",
            credentials=self._get_google_credentials(
                scopes=[
                    "https://www.googleapis.com/auth/admin.directory.customer.readonly"
                ]
            ),
        )
        customer_resource = service.customers()
        request = customer_resource.get(customerKey="my_customer")
        return request.execute()

    def _get_chromeosdevices_service(self):
        service = googleapiclient.discovery.build(
            "admin",
            "directory_v1",
            credentials=self._get_google_credentials(
                scopes=[
                    "https://www.googleapis.com/auth/admin.directory.device.chromeos.readonly",
                    "https://www.googleapis.com/auth/admin.directory.device.chromeos",
                ]
            ),
        )
        return service.chromeosdevices()

    def _get_users_service(self):
        service = googleapiclient.discovery.build(
            "admin",
            "directory_v1",
            credentials=self._get_google_credentials(
                scopes=["https://www.googleapis.com/auth/admin.directory.user.readonly"]
            ),
        )
        return service.users()

    def _extract_from_dictionary(self, dictionary: dict, keys: list):
        value = dictionary
        for key in keys:
            value = value[key]
        return value
