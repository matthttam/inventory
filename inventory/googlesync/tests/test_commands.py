from django.test import TestCase
from parameterized import parameterized
from django.core.management import call_command

from googlesync.management.commands._google_sync import GoogleSyncCommand
from googlesync.exceptions import ConfigNotFound

from googlesync.models import GoogleServiceAccountConfig
from googlesync.tests.factories import GoogleServiceAccountConfigFactory
from unittest.mock import patch, Mock
from io import StringIO
from django.forms import model_to_dict
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import Resource

import pytest


class GoogleSyncMissingConfigTest(TestCase):
    @patch("sys.stdout", new_callable=StringIO)
    @patch(
        "googlesync.management.commands._google_sync.GoogleSyncCommand._get_my_customer"
    )
    def test___init___missing_google_config(self, mock__get_my_customer, mock_stdout):
        """
        Without a google config in the database a ConfigNotFound error should be raised and a message output to std out.
        """
        mock__get_my_customer.return_value = {}
        with self.assertRaises(ConfigNotFound) as context:
            GoogleSyncCommand()
        self.assertEqual(
            mock_stdout.getvalue().strip(), "Failed to find google sync config!"
        )


class GoogleSyncTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        GoogleServiceAccountConfigFactory(delegate="test@example.com")

    def setUp(self):
        self.google_config = GoogleServiceAccountConfig.objects.get(id=1)

    @patch("sys.stdout", new_callable=StringIO)
    @patch(
        "googlesync.management.commands._google_sync.GoogleSyncCommand._get_my_customer"
    )
    def test___init___valid_google_config(self, mock__get_my_customer, mock_stdout):
        """Test that the google_config is stored. Delegate is removed and stored into DELEGATE. and customer is set to result of _get_my_customer()"""
        mock__get_my_customer.return_value = {"test": "value"}
        # GoogleServiceAccountConfigFactory(delegate="test@example.com")
        # google_config = GoogleServiceAccountConfig.objects.get(id=1)
        google_config_dict = model_to_dict(self.google_config)
        del google_config_dict["delegate"]

        command = GoogleSyncCommand()

        self.assertEqual(command.customer, {"test": "value"})
        self.assertEqual(command.google_config, google_config_dict)
        self.assertEqual(command.DELEGATE, "test@example.com")

    @patch("google.oauth2.service_account.Credentials.from_service_account_info")
    @patch(
        "googlesync.management.commands._google_sync.GoogleSyncCommand._get_my_customer"
    )
    def test__get_google_credentials(
        self, mock__get_my_customer, mock_service_account_credentials
    ):
        # Mock Basic Credentials
        mock_credentials = Mock(Credentials)
        mock_service_account_credentials.return_value = mock_credentials

        # Mock Credentials with subject ran
        mock_credentials_with_subject = Mock(Credentials)
        mock_credentials.with_subject.return_value = mock_credentials_with_subject

        command = GoogleSyncCommand()

        # Run get_google_credentials with scopes and verify called_with and return value
        scopes = scopes = ["scope_a", "scope_b"]
        return_value = command._get_google_credentials(scopes)
        self.assertEqual(return_value, mock_credentials_with_subject)
        mock_service_account_credentials.assert_called_with(
            json.loads(json.dumps(command.google_config)), scopes=scopes
        )
        # Verify with_subject was called with the object delegate we expect
        mock_credentials.with_subject.assert_called_with("test@example.com")

    @patch("googleapiclient.discovery.build")
    @patch(
        "googlesync.management.commands._google_sync.GoogleSyncCommand._get_google_credentials"
    )
    def test__get_my_customer(
        self, mock__get_google_credentials, mock_googleapiclient_discovery_build
    ):
        # Mock Basic Credentials
        mock_credentials = Mock(Credentials)
        mock__get_google_credentials.return_value = mock_credentials

        # Mock Service Resource return from build
        mock_resource = Mock()
        mock_googleapiclient_discovery_build.return_value = mock_resource

        # Define mock_resource return
        mock_customer_resource = Mock()
        mock_resource.customers.return_value = mock_customer_resource

        # Define mock_customer_resource return
        mock_request = Mock()
        mock_customer_resource.get.return_value = mock_request

        # Define mock_request execute return
        request_execute_result = Mock()
        mock_request.execute.return_value = request_execute_result

        command = GoogleSyncCommand()
        return_value = command._get_my_customer()

        mock__get_google_credentials.assert_called_with(
            scopes=["https://www.googleapis.com/auth/admin.directory.customer.readonly"]
        )
        mock_googleapiclient_discovery_build.assert_called_with(
            "admin", "directory_v1", credentials=mock_credentials
        )
        mock_resource.customers.assert_called()
        mock_customer_resource.get.assert_called_with(customerKey="my_customer")
        mock_request.execute.assert_called()
        self.assertEqual(return_value, request_execute_result)

    def test__get_chromeosdevices_service(self):
        self.skipTest("May refactor")

    def test__get_users_service(self):
        self.skipTest("May refactor")

    @parameterized.expand(
        [
            ("first level", ["a"], {"b": "b"}),
            ("second level", ["a", "b"], "b"),
            ("next first level", ["aa"], {"bb": {"cc": "cc"}}),
            ("next second level", ["aa", "bb"], {"cc": "cc"}),
            ("next third level", ["aa", "bb", "cc"], "cc"),
        ]
    )
    @patch(
        "googlesync.management.commands._google_sync.GoogleSyncCommand._get_my_customer"
    )
    def test__extract_from_dictionary(
        self, name, keys, expected, mock__get_my_customer
    ):
        command = GoogleSyncCommand()
        dictionary = {
            "a": {"b": "b"},
            "aa": {"bb": {"cc": "cc"}},
        }
        self.assertEqual(
            command._extract_from_dictionary(dictionary=dictionary, keys=keys), expected
        )

    @patch(
        "googlesync.management.commands._google_sync.GoogleSyncCommand._get_my_customer"
    )
    def test__extract_from_dictionary_invalid_key(self, mock__get_my_customer):
        command = GoogleSyncCommand()
        dictionary = {
            "a": {"b": "b"},
            "aa": {"bb": {"cc": "cc"}},
        }
        with self.assertRaises(KeyError):
            command._extract_from_dictionary(dictionary=dictionary, keys=["zz"])

    # @patch("googlesync.management.commands._google_sync.GoogleSyncCommand")
    # @patch("googlesync.management.commands._google_sync.GoogleSyncCommand.__init__")
    # @patch("googlesync.management.commands._google_sync.GoogleSyncCommand._get_customer_service")
    # def test__get_google_config_without_config_raises_config_not_found_error(
    #    self, mock__get_customer_service
    # ):
    #    # sync_command = GoogleSyncCommand()
    #    # with self.assertRaises(ConfigNotFound):
    #    # mock_sync_command._get_google_config()
    #    # dir(mock_sync_command._get_google_config)
    #    mock__get_customer_service.return_value = {""}
    #    mock_init._get_customer_service = None
    #    mock_init.side_effect = lambda self: super().__init__(*args, **kwargs)
    #    sync_command = GoogleSyncCommand()
    #    sync_command._get_google_config()
