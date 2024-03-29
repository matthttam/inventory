import json
from io import StringIO
from unittest.mock import Mock, patch

from django.forms import model_to_dict
from django.test import TestCase
from google.oauth2.service_account import Credentials
from googlesync.exceptions import ConfigNotFound
from googlesync.management.commands._google_sync import GoogleSyncCommandAbstract
from googlesync.management.commands.sync_google_people import (
    Command as GooglePeopleSyncCommand,
)
from googlesync.models import GoogleServiceAccountConfig
from googlesync.tests.factories import (
    GoogleDefaultSchemaPropertyFactory,
    GooglePersonMappingFactory,
    GooglePersonSyncProfileFactory,
    GooglePersonTranslationFactory,
    GoogleServiceAccountConfigFactory,
)
from parameterized import parameterized


class GoogleSyncMissingConfigTest(TestCase):
    @patch("sys.stdout", new_callable=StringIO)
    @patch.object(GoogleSyncCommandAbstract, "_get_my_customer")
    def test___init___missing_google_config(self, mock__get_my_customer, mock_stdout):
        """
        Without a google config in the database a ConfigNotFound error should be raised and a message output to std out.
        """
        mock__get_my_customer.return_value = {}
        with self.assertRaises(ConfigNotFound) as context:
            GoogleSyncCommandAbstract()
        self.assertEqual(str(context.exception), "'Google Sync' config not found.")


class GoogleSyncTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        GoogleServiceAccountConfigFactory(project_id=1, delegate="test@example.com")

    def setUp(self):
        self.google_config = GoogleServiceAccountConfig.objects.get(project_id=1)

    @patch("sys.stdout", new_callable=StringIO)
    @patch.object(GoogleSyncCommandAbstract, "_get_my_customer")
    def test___init___valid_google_config(self, mock__get_my_customer, mock_stdout):
        """Test that the google_config is stored. Delegate is removed and stored into DELEGATE. and customer is set to result of _get_my_customer()"""
        mock__get_my_customer.return_value = {"test": "value"}
        # GoogleServiceAccountConfigFactory(delegate="test@example.com")
        # google_config = GoogleServiceAccountConfig.objects.get(id=1)
        google_config_dict = model_to_dict(self.google_config)
        del google_config_dict["delegate"]

        command = GoogleSyncCommandAbstract()

        self.assertEqual(command.customer, {"test": "value"})
        self.assertEqual(command.google_config, google_config_dict)
        self.assertEqual(command.DELEGATE, "test@example.com")

    @patch.object(Credentials, "from_service_account_info")
    @patch.object(GoogleSyncCommandAbstract, "_get_my_customer")
    def test__get_google_credentials(
        self, mock__get_my_customer, mock_service_account_credentials
    ):
        # Mock Basic Credentials
        mock_credentials = Mock(Credentials)
        mock_service_account_credentials.return_value = mock_credentials

        # Mock Credentials with subject ran
        mock_credentials_with_subject = Mock(Credentials)
        mock_credentials.with_subject.return_value = mock_credentials_with_subject

        command = GoogleSyncCommandAbstract()

        # Run get_google_credentials with scopes and verify called_with and return value
        scopes = scopes = ["scope_a", "scope_b"]
        return_value = command._get_google_credentials(scopes)
        self.assertEqual(return_value, mock_credentials_with_subject)
        mock_service_account_credentials.assert_called_with(
            json.loads(json.dumps(command.google_config)), scopes=scopes
        )
        # Verify with_subject was called with the object delegate we expect
        mock_credentials.with_subject.assert_called_with("test@example.com")

    # @patch("googleapiclient.http.BatchHttpRequest")
    @patch(
        "googlesync.management.commands._google_sync.BatchHttpRequest",
        new_callable=Mock(),
    )
    @patch.object(GoogleSyncCommandAbstract, "_get_my_customer")
    def test__process_batch_requests_batches_by_1000(
        self, mock__get_my_customer, mock_BatchHttpRequest
    ):
        def batch_side_effect():
            return Mock()

        requests = list(range(0, 2001))
        mock_batch = Mock(**{"execute.side_effect": batch_side_effect()})
        mock_BatchHttpRequest.return_value = mock_batch
        mock_service = Mock()

        command = GoogleSyncCommandAbstract()
        responses = command._process_batch_requests(
            service=mock_service, requests=requests, callback=None
        )
        mock_BatchHttpRequest.assert_any_call(
            callback=None, batch_uri="https://www.googleapis.com/batch/admin/v1"
        )
        self.assertEqual(mock_BatchHttpRequest.call_count, 3)
        self.assertEqual(mock_batch.add.call_count, 2001)
        self.assertEqual(mock_batch.execute.call_count, 3)
        self.assertEqual(len(responses), 3)

    @patch.object(GoogleSyncCommandAbstract, "_get_customer_service")
    def test__get_my_customer(self, mock__get_customer_service):
        mock_customer_resource = Mock()
        mock_request = Mock()
        mock_request_execute_result = Mock()
        mock__get_customer_service.return_value = mock_customer_resource
        mock_customer_resource.get.return_value = mock_request
        mock_request.execute.return_value = mock_request_execute_result

        command = GoogleSyncCommandAbstract()
        return_value = command._get_my_customer()

        mock_customer_resource.get.assert_called_with(customerKey="my_customer")
        mock_request.execute.assert_called()

        self.assertEqual(return_value, mock_request_execute_result)

    def test__get_customer_service(self):
        mock_resource = Mock()
        mock_service = Mock()
        mock_service.customers.return_value = mock_resource

        with patch.object(
            GoogleSyncCommandAbstract, "_get_service", return_value=mock_service
        ) as mock_get_service:
            command = GoogleSyncCommandAbstract()
            return_value = command._get_customer_service()
            mock_get_service.assert_called_with(
                "https://www.googleapis.com/auth/admin.directory.customer.readonly"
            )
            mock_service.customers.assert_called()
            self.assertEqual(return_value, mock_resource)

    def test__get_chromeosdevices_service(self):
        mock_resource = Mock()
        mock_service = Mock()
        mock_service.chromeosdevices.return_value = mock_resource

        with patch.object(
            GoogleSyncCommandAbstract, "_get_service", return_value=mock_service
        ) as mock_get_service:
            command = GoogleSyncCommandAbstract()
            return_value = command._get_chromeosdevices_service()
            mock_get_service.assert_called_with(
                [
                    "https://www.googleapis.com/auth/admin.directory.device.chromeos.readonly",
                    "https://www.googleapis.com/auth/admin.directory.device.chromeos",
                ]
            )
            mock_service.chromeosdevices.assert_called()
            self.assertEqual(return_value, mock_resource)

    def test__get_users_service(self):
        mock_resource = Mock()
        mock_service = Mock()
        mock_service.users.return_value = mock_resource

        with patch.object(
            GoogleSyncCommandAbstract, "_get_service", return_value=mock_service
        ) as mock_get_service:
            command = GoogleSyncCommandAbstract()
            return_value = command._get_users_service()
            mock_get_service.assert_called_with(
                "https://www.googleapis.com/auth/admin.directory.user.readonly"
            )
            mock_service.users.assert_called()
            self.assertEqual(return_value, mock_resource)

    def test__get_schemas_service(self):
        mock_resource = Mock()
        mock_service = Mock()
        mock_service.schemas.return_value = mock_resource

        with patch.object(
            GoogleSyncCommandAbstract, "_get_service", return_value=mock_service
        ) as mock_get_service:
            command = GoogleSyncCommandAbstract()
            return_value = command._get_schemas_service()
            mock_get_service.assert_called_with(
                "https://www.googleapis.com/auth/admin.directory.userschema.readonly"
            )
            mock_service.schemas.assert_called()
            self.assertEqual(return_value, mock_resource)

    def test__get_schema_by_name(self):
        self.skipTest("Need to test")

    @patch("googleapiclient.discovery.build")
    @patch.object(GoogleSyncCommandAbstract, "_get_google_credentials")
    def test__get_service(
        self, mock__get_google_credentials, mock_googleapiclient_discovery_build
    ):
        # Mock Basic Credentials
        mock_credentials = Mock(Credentials)
        mock__get_google_credentials.return_value = mock_credentials
        # Mock discovery.build
        mock_service = Mock()
        mock_googleapiclient_discovery_build.return_value = mock_service

        # Mock discovery.build
        mock_service = Mock()
        mock_googleapiclient_discovery_build.return_value = mock_service

        command = GoogleSyncCommandAbstract()
        return_value = command._get_service("test_scope")
        mock__get_google_credentials.assert_called_with(scopes=["test_scope"])
        mock_googleapiclient_discovery_build.assert_called_with(
            "admin", "directory_v1", credentials=mock_credentials
        )
        self.assertEqual(return_value, mock_service)

    @parameterized.expand(
        [
            ("first level", ["a"], {"b": "b"}),
            ("second level", ["a", "b"], "b"),
            ("next first level", ["aa"], {"bb": {"cc": "cc"}}),
            ("next second level", ["aa", "bb"], {"cc": "cc"}),
            ("next third level", ["aa", "bb", "cc"], "cc"),
        ]
    )
    @patch.object(GoogleSyncCommandAbstract, "_get_my_customer")
    def test__extract_from_dictionary(
        self, name, keys, expected, mock__get_my_customer
    ):
        command = GoogleSyncCommandAbstract()
        dictionary = {
            "a": {"b": "b"},
            "aa": {"bb": {"cc": "cc"}},
        }
        self.assertEqual(
            command._extract_from_dictionary(dictionary=dictionary, keys=keys), expected
        )

    @patch.object(GoogleSyncCommandAbstract, "_get_my_customer")
    def test__extract_from_dictionary_invalid_key_throws_key_error(
        self, mock__get_my_customer
    ):
        command = GoogleSyncCommandAbstract()
        dictionary = {
            "a": {"b": "b"},
            "aa": {"bb": {"cc": "cc"}},
        }
        with self.assertRaises(KeyError):
            command._extract_from_dictionary(dictionary=dictionary, keys=["zz"])

    @patch.object(GoogleSyncCommandAbstract, "_get_my_customer")
    def test__extract_from_dictionary_blank_key_returns_none(
        self, mock__get_my_customer
    ):
        command = GoogleSyncCommandAbstract()
        dictionary = {
            "a": {"b": "b"},
            "aa": {"bb": {"cc": "cc"}},
        }
        # with self.assertRaises(KeyError):
        self.assertIsNone(
            command._extract_from_dictionary(dictionary=dictionary, keys=[])
        )

    @patch.object(GoogleSyncCommandAbstract, "_get_my_customer")
    def test__map_dictionary(self, mock__get_my_customer):
        sync_profile = GooglePersonSyncProfileFactory()
        google_default_schema_property = GoogleDefaultSchemaPropertyFactory(
            etag="fromfield"
        )
        GooglePersonMappingFactory(
            sync_profile=sync_profile,
            from_field=google_default_schema_property,
            to_field="tofield",
        )
        google_user = {"fromfield": "fromfieldvalue"}
        command = GooglePeopleSyncCommand()
        return_value = command._map_dictionary(sync_profile, google_user)
        self.assertEqual(return_value, {"tofield": "fromfieldvalue"})

    @patch.object(GoogleSyncCommandAbstract, "_get_my_customer")
    def test__map_dictionary_with_translations(self, mock__get_my_customer):
        sync_profile = GooglePersonSyncProfileFactory()

        # Create a mapping with a translation
        google_default_schema_property = GoogleDefaultSchemaPropertyFactory(
            etag="fromfield"
        )
        mapping = GooglePersonMappingFactory(
            sync_profile=sync_profile,
            from_field=google_default_schema_property,
            to_field="tofield",
        )
        GooglePersonTranslationFactory(
            google_person_mapping=mapping,
            translate_from="replace_me",
            translate_to="with_this",
        )
        # Create a mapping with dot notation
        google_default_schema_property_name = GoogleDefaultSchemaPropertyFactory(
            etag="name",
        )
        google_default_schema_property_first = GoogleDefaultSchemaPropertyFactory(
            etag="first",
            parent=google_default_schema_property_name,
        )
        GooglePersonMappingFactory(
            sync_profile=sync_profile,
            from_field=google_default_schema_property_first,
            to_field="firstname",
        )

        google_user = {"fromfield": "replace_me", "name": {"first": "Doug"}}

        expected_output = {"tofield": "with_this", "firstname": "Doug"}
        command = GoogleSyncCommandAbstract()
        return_value = command._map_dictionary(sync_profile, google_user)
        self.assertEqual(return_value, expected_output)

    def test__convert_to_type(self):
        self.skipTest("Need to test")

    def test__initialize_custom_schemas(self):
        self.skipTest("Need to test")

    def test__delete_default_schemas(self):
        self.skipTest("Need to test")

    def test__initialize_default_schema(self):
        self.skipTest("Need to test")
