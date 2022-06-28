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
        customer_service = self._get_customer_service()
        request = customer_service.get(customerKey="my_customer")
        self.customer = request.execute()

    def _get_google_config(self) -> dict:
        try:
            google_config = model_to_dict(GoogleServiceAccountConfig.objects.first())
        except AttributeError:
            self.stdout.write(self.style.ERROR("Failed to find google sync config!"))
            raise ConfigNotFound(config_name="Google Sync")

        return google_config

    def _get_google_credentials(self, scopes: list):
        # Verify service account google config exists
        google_config = self._get_google_config()

        self.DELEGATE = google_config.pop("delegate")
        # Parse the config into a json string and load it into a json object
        service_account_info = json.loads(json.dumps(google_config))
        credentials = service_account.Credentials.from_service_account_info(
            service_account_info, scopes=scopes
        )

        credentials_delegated = credentials.with_subject(self.DELEGATE)

        return credentials_delegated

    def _get_customer_service(self):
        SCOPES = ["https://www.googleapis.com/auth/admin.directory.customer.readonly"]
        credentials = self._get_google_credentials(scopes=SCOPES)
        service = googleapiclient.discovery.build(
            "admin", "directory_v1", credentials=credentials
        )
        return service.customers()

    def _get_chromeosdevices_service(self):
        SCOPES = [
            "https://www.googleapis.com/auth/admin.directory.device.chromeos.readonly",
            "https://www.googleapis.com/auth/admin.directory.device.chromeos",
        ]
        credentials = self._get_google_credentials(scopes=SCOPES)
        service = googleapiclient.discovery.build(
            "admin", "directory_v1", credentials=credentials
        )
        return service.chromeosdevices()

    def _get_users_service(self):
        SCOPES = ["https://www.googleapis.com/auth/admin.directory.user.readonly"]
        credentials = self._get_google_credentials(scopes=SCOPES)
        service = googleapiclient.discovery.build(
            "admin", "directory_v1", credentials=credentials
        )
        return service.users()

    def _extract_from_dictionary(self, dictionary: dict, keys: list):
        value = dictionary
        for key in keys:
            value = value[key]
        return value
