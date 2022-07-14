from django.core.management.base import BaseCommand, CommandError

from google.oauth2 import service_account
import googleapiclient.discovery
import json

from django.forms import model_to_dict
from googlesync.models import GoogleServiceAccountConfig, GoogleSyncProfileAbstract
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
        customer_resource = self._get_customer_service()
        request = customer_resource.get(customerKey="my_customer")
        return request.execute()

    def _get_customer_service(self):
        service = googleapiclient.discovery.build(
            "admin",
            "directory_v1",
            credentials=self._get_google_credentials(
                scopes=[
                    "https://www.googleapis.com/auth/admin.directory.customer.readonly"
                ]
            ),
        )
        return service.customers()

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
        if not keys:
            return None
        value = dictionary
        for key in keys:
            value = value[key]
        return value

    def _map_dictionary(
        self, sync_profile: GoogleSyncProfileAbstract, object_dictionary: dict
    ) -> dict:
        mappings = list(sync_profile.mappings.all())
        new_dictionary = {}
        for mapping in mappings:
            try:
                new_dictionary[mapping.to_field] = self._extract_from_dictionary(
                    object_dictionary, mapping.from_field.split(".")
                )
            except KeyError:
                new_dictionary[mapping.to_field] = None

            # Use translations to convert one value to another
            translations = list(mapping.translations.all())
            # translations = GooglePersonTranslation.objects.filter(
            #    google_person_mapping=mapping
            # )

            for translation in translations:
                if str(new_dictionary[mapping.to_field]) == translation.translate_from:
                    new_dictionary[mapping.to_field] = translation.translate_to
        return new_dictionary
