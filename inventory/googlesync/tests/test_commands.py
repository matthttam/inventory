from django.core.management.base import BaseCommand
from django.test import TestCase
from parameterized import parameterized
from django.core.management import call_command

from googlesync.management.commands._google_sync import GoogleSyncCommand
from googlesync.management.commands.sync_google_devices import (
    Command as GoogleDevicesSyncCommand,
)
from googlesync.management.commands.link_google_devices import (
    Command as GoogleDevicesLinkCommand,
)
from googlesync.management.commands.sync_google_people import (
    Command as GooglePeopleSyncCommand,
)
from googlesync.exceptions import ConfigNotFound, SyncProfileNotFound

from googlesync.models import (
    GooglePersonSyncProfile,
    GoogleServiceAccountConfig,
    GoogleDeviceSyncProfile,
    GoogleDevice,
)
from googlesync.tests.factories import (
    GoogleConfigFactory,
    GoogleDeviceSyncProfileFactory,
    GooglePersonMappingFactory,
    GooglePersonSyncProfileFactory,
    GooglePersonTranslationFactory,
    GoogleServiceAccountConfigFactory,
    GoogleDeviceFactory,
)
from unittest.mock import MagicMock, call, patch, Mock
from io import StringIO
from django.forms import model_to_dict
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import Resource
import pytest

from people.tests.factories import PersonFactory, PersonStatusFactory, PersonTypeFactory
from people.models import Person


class GoogleSyncMissingConfigTest(TestCase):
    @patch("sys.stdout", new_callable=StringIO)
    @patch.object(GoogleSyncCommand, "_get_my_customer")
    def test___init___missing_google_config(self, mock__get_my_customer, mock_stdout):
        """
        Without a google config in the database a ConfigNotFound error should be raised and a message output to std out.
        """
        mock__get_my_customer.return_value = {}
        with self.assertRaises(ConfigNotFound) as context:
            GoogleSyncCommand()
        self.assertEqual(str(context.exception), "'Google Sync' config not found.")


class GoogleSyncTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        GoogleServiceAccountConfigFactory(project_id=1, delegate="test@example.com")

    def setUp(self):
        self.google_config = GoogleServiceAccountConfig.objects.get(project_id=1)

    @patch("sys.stdout", new_callable=StringIO)
    @patch.object(GoogleSyncCommand, "_get_my_customer")
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

    @patch.object(Credentials, "from_service_account_info")
    @patch.object(GoogleSyncCommand, "_get_my_customer")
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

    @patch.object(GoogleSyncCommand, "_get_customer_service")
    def test__get_my_customer(self, mock__get_customer_service):
        mock_customer_resource = Mock()
        mock_request = Mock()
        mock_request_execute_result = Mock()
        mock__get_customer_service.return_value = mock_customer_resource
        mock_customer_resource.get.return_value = mock_request
        mock_request.execute.return_value = mock_request_execute_result

        command = GoogleSyncCommand()
        return_value = command._get_my_customer()

        mock_customer_resource.get.assert_called_with(customerKey="my_customer")
        mock_request.execute.assert_called()

        self.assertEqual(return_value, mock_request_execute_result)

    @patch("googleapiclient.discovery.build")
    @patch.object(GoogleSyncCommand, "_get_google_credentials")
    def test__get_customer_service(
        self, mock__get_google_credentials, mock_googleapiclient_discovery_build
    ):

        mock_credentials = Mock(Credentials)
        mock_resource = Mock()
        mock_customer_resource = Mock()

        mock__get_google_credentials.return_value = mock_credentials
        mock_googleapiclient_discovery_build.return_value = mock_resource
        mock_resource.customers.return_value = mock_customer_resource

        command = GoogleSyncCommand()
        return_value = command._get_customer_service()

        mock__get_google_credentials.assert_called_with(
            scopes=["https://www.googleapis.com/auth/admin.directory.customer.readonly"]
        )
        mock_googleapiclient_discovery_build.assert_called_with(
            "admin", "directory_v1", credentials=mock_credentials
        )
        mock_resource.customers.assert_called()
        self.assertEqual(return_value, mock_customer_resource)

    @patch("googleapiclient.discovery.build")
    @patch.object(GoogleSyncCommand, "_get_google_credentials")
    def test__get_chromeosdevices_service(
        self, mock__get_google_credentials, mock_googleapiclient_discovery_build
    ):
        # Mock Basic Credentials
        mock_credentials = Mock(Credentials)
        mock_service = Mock()
        mock_chromeosdevices_resource = Mock()

        mock__get_google_credentials.return_value = mock_credentials
        mock_googleapiclient_discovery_build.return_value = mock_service
        mock_service.chromeosdevices.return_value = mock_chromeosdevices_resource

        command = GoogleSyncCommand()
        return_value = command._get_chromeosdevices_service()

        mock__get_google_credentials.assert_called_with(
            scopes=[
                "https://www.googleapis.com/auth/admin.directory.device.chromeos.readonly",
                "https://www.googleapis.com/auth/admin.directory.device.chromeos",
            ]
        )
        mock_googleapiclient_discovery_build.assert_called_with(
            "admin", "directory_v1", credentials=mock_credentials
        )
        mock_service.chromeosdevices.assert_called_with()
        self.assertEqual(return_value, mock_chromeosdevices_resource)

    @patch("googleapiclient.discovery.build")
    @patch.object(GoogleSyncCommand, "_get_google_credentials")
    def test__get_users_service(
        self, mock__get_google_credentials, mock_googleapiclient_discovery_build
    ):
        # Mock Basic Credentials
        mock_credentials = Mock(Credentials)
        mock__get_google_credentials.return_value = mock_credentials

        # Mock discovery.build
        mock_service = Mock()
        mock_googleapiclient_discovery_build.return_value = mock_service

        # Mock resource
        mock_users_resource = Mock()
        mock_service.users.return_value = mock_users_resource

        command = GoogleSyncCommand()
        return_value = command._get_users_service()

        mock__get_google_credentials.assert_called_with(
            scopes=["https://www.googleapis.com/auth/admin.directory.user.readonly"]
        )
        mock_googleapiclient_discovery_build.assert_called_with(
            "admin", "directory_v1", credentials=mock_credentials
        )
        mock_service.users.assert_called_with()
        self.assertEqual(return_value, mock_users_resource)

    @parameterized.expand(
        [
            ("first level", ["a"], {"b": "b"}),
            ("second level", ["a", "b"], "b"),
            ("next first level", ["aa"], {"bb": {"cc": "cc"}}),
            ("next second level", ["aa", "bb"], {"cc": "cc"}),
            ("next third level", ["aa", "bb", "cc"], "cc"),
        ]
    )
    @patch.object(GoogleSyncCommand, "_get_my_customer")
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

    @patch.object(GoogleSyncCommand, "_get_my_customer")
    def test__extract_from_dictionary_invalid_key_throws_key_error(
        self, mock__get_my_customer
    ):
        command = GoogleSyncCommand()
        dictionary = {
            "a": {"b": "b"},
            "aa": {"bb": {"cc": "cc"}},
        }
        with self.assertRaises(KeyError):
            command._extract_from_dictionary(dictionary=dictionary, keys=["zz"])

    @patch.object(GoogleSyncCommand, "_get_my_customer")
    def test__extract_from_dictionary_blank_key_returns_none(
        self, mock__get_my_customer
    ):
        command = GoogleSyncCommand()
        dictionary = {
            "a": {"b": "b"},
            "aa": {"bb": {"cc": "cc"}},
        }
        # with self.assertRaises(KeyError):
        self.assertIsNone(
            command._extract_from_dictionary(dictionary=dictionary, keys=[])
        )

    @patch.object(GoogleSyncCommand, "_get_my_customer")
    def test__map_dictionary(self, mock__get_my_customer):
        sync_profile = GooglePersonSyncProfileFactory()
        GooglePersonMappingFactory(
            sync_profile=sync_profile, from_field="fromfield", to_field="tofield"
        )
        google_user = {"fromfield": "fromfieldvalue"}
        command = GooglePeopleSyncCommand()
        return_value = command._map_dictionary(sync_profile, google_user)
        self.assertEqual(return_value, {"tofield": "fromfieldvalue"})

    @patch.object(GoogleSyncCommand, "_get_my_customer")
    def test__map_dictionary_with_translations(self, mock__get_my_customer):
        sync_profile = GooglePersonSyncProfileFactory()
        # Create a mapping with a translation
        mapping = GooglePersonMappingFactory(
            sync_profile=sync_profile, from_field="fromfield", to_field="tofield"
        )
        GooglePersonTranslationFactory(
            google_person_mapping=mapping,
            translate_from="replace_me",
            translate_to="with_this",
        )
        # Create a mapping with dot notation
        GooglePersonMappingFactory(
            sync_profile=sync_profile, from_field="name.first", to_field="firstname"
        )

        google_user = {"fromfield": "replace_me", "name": {"first": "Doug"}}
        command = GoogleSyncCommand()
        return_value = command._map_dictionary(sync_profile, google_user)
        self.assertEqual(return_value, {"tofield": "with_this", "firstname": "Doug"})


class SyncGooglePeopleTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        GoogleServiceAccountConfigFactory(project_id=1, delegate="test@example.com")

    def setUp(self):
        self.google_config = GoogleServiceAccountConfig.objects.get(project_id=1)

        # Mock the _get_my_customer call used in GoogleSyncCommand __init__
        mock_customer_resource = Mock()
        patcher__get_my_customer = patch.object(GoogleSyncCommand, "_get_my_customer")

        self.addCleanup(patcher__get_my_customer.stop)
        self.mock__get_my_customer = patcher__get_my_customer.start()
        self.mock__get_my_customer.return_value = mock_customer_resource

    def test_subclass(self):
        self.assertTrue(issubclass(GooglePeopleSyncCommand, GoogleSyncCommand))

    def test_help(self):
        self.assertEqual(
            GooglePeopleSyncCommand.help, "Syncs google users to inventory people."
        )

    @patch.object(GooglePeopleSyncCommand, "sync_google_people")
    def test__get_person_sync_profile_invalid_names(self, mock_sync_google_people):
        with self.assertRaises(SyncProfileNotFound) as context:
            call_command("sync_google_people", "random_profile")
        self.assertEqual(str(context.exception), "'random_profile' profile not found")

        GooglePersonSyncProfileFactory(name="real_sync_profile")
        with self.assertRaises(SyncProfileNotFound) as context:
            call_command("sync_google_people", "real_sync_profile", "fake_sync_profile")
        self.assertEqual(
            str(context.exception), "'fake_sync_profile' profile not found"
        )
        mock_sync_google_people.assert_not_called()

    @patch.object(GooglePeopleSyncCommand, "sync_google_people")
    def test__get_person_sync_profile_valid_names(self, mock_sync_google_people):
        GooglePersonSyncProfileFactory(name="real_sync_profile")
        GooglePersonSyncProfileFactory(name="another_real_sync_profile")
        google_person_sync1 = GooglePersonSyncProfile.objects.get(
            name="real_sync_profile"
        )
        google_person_sync2 = GooglePersonSyncProfile.objects.get(
            name="another_real_sync_profile"
        )

        call_command("sync_google_people", "real_sync_profile")

        mock_sync_google_people.assert_called_with(google_person_sync1)
        mock_sync_google_people.asssert_not_called_with(google_person_sync2)

        mock_sync_google_people.reset_mock()
        call_command(
            "sync_google_people", "real_sync_profile", "another_real_sync_profile"
        )
        self.assertEqual(mock_sync_google_people.call_count, 2)

        mock_sync_google_people.assert_has_calls(
            [call(google_person_sync1), call(google_person_sync2)]
        )

    @patch.object(GooglePeopleSyncCommand, "_get_users_service")
    def test__get_google_records_with_domain(self, mock__get_users_service):
        response_get_sideffect = []
        mock_response = Mock(**{"get.side_effect": response_get_sideffect})
        mock_request = Mock(**{"execute.return_value": mock_response})
        user_list_next_sideffect = [None]
        mock_user_service = Mock(
            **{
                "list.return_value": mock_request,
                "list_next.side_effect": user_list_next_sideffect,
            }
        )
        mock__get_users_service.return_value = mock_user_service

        # Testing with three results
        GooglePersonSyncProfileFactory(
            name="staff", google_query="test_query", domain="testdomain.com"
        )
        sync_profile = GooglePersonSyncProfile.objects.get(name="staff")
        command = GooglePeopleSyncCommand()
        query = sync_profile.google_query
        domain = sync_profile.domain
        return_value = command._get_google_records(query=query, domain=domain)

        mock__get_users_service.assert_called_once()
        mock_user_service.list.assert_called_with(
            domain=domain,
            projection="full",
            query=query,
        )

    @patch.object(GooglePeopleSyncCommand, "_get_users_service")
    def test__get_google_records_without_domain(self, mock__get_users_service):
        response_get_sideffect = [None]
        mock_response = Mock(**{"get.side_effect": response_get_sideffect})
        mock_request = Mock(**{"execute.return_value": mock_response})
        user_list_next_sideffect = [None]
        mock_user_service = Mock(
            **{
                "list.return_value": mock_request,
                "list_next.side_effect": user_list_next_sideffect,
            }
        )
        mock__get_users_service.return_value = mock_user_service

        # Testing with three results
        GooglePersonSyncProfileFactory(
            name="staff", google_query="test_query", domain=""
        )
        sync_profile = GooglePersonSyncProfile.objects.get(name="staff")
        command = GooglePeopleSyncCommand()
        query = sync_profile.google_query
        domain = sync_profile.domain
        return_value = command._get_google_records(query=query, domain=domain)

        mock__get_users_service.assert_called_once()
        mock_user_service.list.assert_called_with(
            customer=command.customer.get("id"),
            projection="full",
            query=query,
        )

    @patch.object(GooglePeopleSyncCommand, "_get_users_service")
    def test__get_google_records_with_domain(self, mock__get_users_service):
        pass

    @patch.object(GooglePeopleSyncCommand, "_get_users_service")
    def test__get_google_records(self, mock__get_users_service):
        response_get_sideffect = [
            [{"a": "a", "b": "b", "c": "c"}],
            [{"a": "a", "b": "b", "c": "c"}],
            [{"a": "a", "b": "b", "c": "c"}],
        ]
        mock_response = Mock(**{"get.side_effect": response_get_sideffect})
        mock_request = Mock(**{"execute.return_value": mock_response})
        user_list_next_sideffect = [mock_request, mock_request, None]
        mock_user_service = Mock(
            **{
                "list.return_value": mock_request,
                "list_next.side_effect": user_list_next_sideffect,
            }
        )
        mock__get_users_service.return_value = mock_user_service

        # Testing with three results
        GooglePersonSyncProfileFactory(name="staff", google_query="test_query")
        sync_profile = GooglePersonSyncProfile.objects.get(name="staff")
        command = GooglePeopleSyncCommand()
        query = sync_profile.google_query
        domain = sync_profile.domain
        return_value = command._get_google_records(query=query, domain=domain)

        mock__get_users_service.assert_called_once()
        mock_user_service.list.assert_called_with(
            domain=domain,
            projection="full",
            query=query,
        )
        mock_request.execute.assert_called()
        mock_response.get.assert_called_with("users")
        mock_user_service.list_next.assert_called_with(mock_request, mock_response)
        self.assertEqual(return_value, sum(response_get_sideffect, []))

    @patch.object(GooglePeopleSyncCommand, "_get_users_service")
    def test__get_google_records_no_results(self, mock__get_users_service):

        mock_response = Mock(**{"get.return_value": []})
        mock_request = Mock(**{"execute.return_value": mock_response})
        mock_user_service = Mock(**{"list.return_value": mock_request})
        mock__get_users_service.return_value = mock_user_service

        # Testing with three results
        GooglePersonSyncProfileFactory(name="staff", google_query="test_query")
        sync_profile = GooglePersonSyncProfile.objects.get(name="staff")
        command = GooglePeopleSyncCommand()
        query = sync_profile.google_query
        domain = sync_profile.domain
        return_value = command._get_google_records(query=query, domain=domain)

        mock__get_users_service.assert_called_once()
        mock_user_service.list.assert_called_with(
            projection="full",
            query=query,
            domain=domain,
        )
        mock_request.execute.assert_called()
        mock_response.get.assert_called_with("users")
        mock_user_service.list_next.assert_not_called()
        self.assertEqual(return_value, None)

    @patch.object(GooglePeopleSyncCommand, "convert_google_user_to_person")
    def test_convert_google_users_to_person(self, mock_convert_google_user_to_person):
        person1 = Mock(Person)
        person2 = Mock(Person)
        person3 = Mock(Person)
        google_people = [person1, person2, person3]
        mock_convert_google_user_to_person.side_effect = google_people

        GooglePersonSyncProfileFactory(name="staff", google_query="test_query")
        sync_profile = GooglePersonSyncProfile.objects.get(name="staff")
        google_users = [{"user": "user1"}, {"user": "user2"}, {"user": "user3"}]
        command = GooglePeopleSyncCommand()
        return_value = command.convert_google_users_to_person(
            sync_profile=sync_profile, google_users=google_users
        )
        mock_convert_google_user_to_person.assert_has_calls(
            [
                call(sync_profile, {"user": "user1"}),
                call(sync_profile, {"user": "user2"}),
                call(sync_profile, {"user": "user3"}),
            ]
        )
        self.assertEqual(return_value, google_people)

    @patch.object(GooglePeopleSyncCommand, "_map_dictionary")
    def test_convert_google_user_to_person_valid_user(self, mock__map_dictionary):
        person_status = PersonStatusFactory(name="Active")
        person_dictionary = model_to_dict(PersonFactory.build(google_id="123456789"))
        person_dictionary["status"] = person_status.name
        mock__map_dictionary.return_value = person_dictionary
        person_type = PersonTypeFactory(name="Staff")
        sync_profile = GooglePersonSyncProfileFactory(
            name="staff", google_query="test_query", person_type=person_type
        )
        sync_profile = GooglePersonSyncProfile.objects.get(name="staff")

        command = GooglePeopleSyncCommand()
        # google_user doesn't matter since we are mocking the return of _map_dictionary
        return_value = command.convert_google_user_to_person(
            sync_profile=sync_profile, google_user={}
        )
        self.assertIsInstance(return_value, Person)
        person = Person(**person_dictionary)
        person.type = sync_profile.person_type
        person.status = person_status
        person._buildings = None
        person._rooms = None

        for field in [p.name for p in Person._meta.concrete_fields]:
            self.assertEqual(getattr(person, field), getattr(return_value, field))

    def test_sync_google_people(self):
        self.skipTest("Need to test")


class SyncGoogleDevicesTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        GoogleServiceAccountConfigFactory(project_id=1, delegate="test@example.com")

    def setUp(self):
        self.google_config = GoogleServiceAccountConfig.objects.get(project_id=1)

        # Mock the _get_my_customer call used in GoogleSyncCommand __init__
        mock_customer_resource = Mock()
        patcher__get_my_customer = patch.object(GoogleSyncCommand, "_get_my_customer")

        self.addCleanup(patcher__get_my_customer.stop)
        self.mock__get_my_customer = patcher__get_my_customer.start()
        self.mock__get_my_customer.return_value = mock_customer_resource

    def test_subclass(self):
        self.assertTrue(issubclass(GoogleDevicesSyncCommand, GoogleSyncCommand))

    def test_help(self):
        self.assertEqual(
            GoogleDevicesSyncCommand.help, "Syncs google devices to inventory devices."
        )

    @patch.object(GoogleDevicesSyncCommand, "sync_google_devices")
    def test__get_device_sync_profile_invalid_names(self, mock_sync_google_devices):
        with self.assertRaises(SyncProfileNotFound) as context:
            call_command("sync_google_devices", "random_profile")
        self.assertEqual(str(context.exception), "'random_profile' profile not found")

        GoogleDeviceSyncProfileFactory(name="real_sync_profile")
        with self.assertRaises(SyncProfileNotFound) as context:
            call_command(
                "sync_google_devices", "real_sync_profile", "fake_sync_profile"
            )
        self.assertEqual(
            str(context.exception), "'fake_sync_profile' profile not found"
        )
        mock_sync_google_devices.assert_not_called()

    @patch.object(GoogleDevicesSyncCommand, "sync_google_devices")
    def test__get_device_sync_profile_valid_names(self, mock_sync_google_devices):
        GoogleDeviceSyncProfileFactory(name="real_sync_profile")
        GoogleDeviceSyncProfileFactory(name="another_real_sync_profile")
        google_device_sync1 = GoogleDeviceSyncProfile.objects.get(
            name="real_sync_profile"
        )
        google_device_sync2 = GoogleDeviceSyncProfile.objects.get(
            name="another_real_sync_profile"
        )

        call_command("sync_google_devices", "real_sync_profile")

        mock_sync_google_devices.assert_called_with(google_device_sync1)
        mock_sync_google_devices.asssert_not_called_with(google_device_sync2)

        mock_sync_google_devices.reset_mock()
        call_command(
            "sync_google_devices", "real_sync_profile", "another_real_sync_profile"
        )
        self.assertEqual(mock_sync_google_devices.call_count, 2)

        mock_sync_google_devices.assert_has_calls(
            [call(google_device_sync1), call(google_device_sync2)]
        )

    @patch.object(GoogleDevicesSyncCommand, "_get_chromeosdevices_service")
    def test__get_google_records(self, mock__get_chromeosdevices_service):
        response_get_sideffect = [
            [{"a": "a", "b": "b", "c": "c"}],
            [{"a": "a", "b": "b", "c": "c"}],
            [{"a": "a", "b": "b", "c": "c"}],
        ]
        mock_response = Mock(**{"get.side_effect": response_get_sideffect})
        mock_request = Mock(**{"execute.return_value": mock_response})
        device_list_next_sideffect = [mock_request, mock_request, None]
        mock_device_service = Mock(
            **{
                "list.return_value": mock_request,
                "list_next.side_effect": device_list_next_sideffect,
            }
        )
        mock__get_chromeosdevices_service.return_value = mock_device_service

        # Testing with three results
        GoogleDeviceSyncProfileFactory(name="staff", google_query="test_query")
        sync_profile = GoogleDeviceSyncProfile.objects.get(name="staff")
        command = GoogleDevicesSyncCommand()
        query = sync_profile.google_query
        org_unit_path = sync_profile.google_org_unit_path
        return_value = command._get_google_records(
            query=query, org_unit_path=org_unit_path
        )

        mock__get_chromeosdevices_service.assert_called_once()
        mock_device_service.list.assert_called_with(
            customerId=command.customer.get("id"),
            projection="FULL",
            query=query,
            orgUnitPath=org_unit_path,
        )
        mock_request.execute.assert_called()
        mock_response.get.assert_called_with("chromeosdevices")
        mock_device_service.list_next.assert_called_with(mock_request, mock_response)
        self.assertEqual(return_value, sum(response_get_sideffect, []))

    @patch.object(GoogleDevicesSyncCommand, "_get_chromeosdevices_service")
    def test__get_google_records_no_results(self, mock__get_chromeosdevices_service):

        mock_response = Mock(**{"get.return_value": []})
        mock_request = Mock(**{"execute.return_value": mock_response})
        mock_user_service = Mock(**{"list.return_value": mock_request})
        mock__get_chromeosdevices_service.return_value = mock_user_service

        # Testing with three results
        GoogleDeviceSyncProfileFactory(name="staff", google_query="test_query")
        sync_profile = GoogleDeviceSyncProfile.objects.get(name="staff")
        command = GoogleDevicesSyncCommand()
        query = sync_profile.google_query
        org_unit_path = sync_profile.google_org_unit_path
        return_value = command._get_google_records(
            query=query, org_unit_path=org_unit_path
        )

        mock__get_chromeosdevices_service.assert_called_once()
        mock_user_service.list.assert_called_with(
            customerId=command.customer.get("id"),
            projection="FULL",
            query=query,
            orgUnitPath=org_unit_path,
        )
        mock_request.execute.assert_called()
        mock_response.get.assert_called_with("chromeosdevices")
        mock_user_service.list_next.assert_not_called()
        self.assertEqual(return_value, None)

    @patch.object(GoogleDevicesSyncCommand, "convert_google_device_to_google_device")
    def test_convert_google_devices_to_google_devices(
        self, mock_convert_google_device_to_google_device
    ):
        device1 = Mock(GoogleDevice)
        device2 = Mock(GoogleDevice)
        device3 = Mock(GoogleDevice)
        google_devices = [device1, device2, device3]
        mock_convert_google_device_to_google_device.side_effect = google_devices

        GoogleDeviceSyncProfileFactory(name="staff", google_query="test_query")
        sync_profile = GoogleDeviceSyncProfile.objects.get(name="staff")
        google_devices_dict = [
            {"device": "device1"},
            {"device": "device2"},
            {"device": "device3"},
        ]
        command = GoogleDevicesSyncCommand()
        return_value = command.convert_google_devices_to_google_devices(
            sync_profile=sync_profile, google_devices=google_devices_dict
        )
        mock_convert_google_device_to_google_device.assert_has_calls(
            [
                call(sync_profile, {"device": "device1"}),
                call(sync_profile, {"device": "device2"}),
                call(sync_profile, {"device": "device3"}),
            ]
        )
        self.assertEqual(return_value, google_devices)

    @patch.object(GoogleDevicesSyncCommand, "_map_dictionary")
    def test_convert_google_device_to_device_valid_google_device(
        self, mock__map_dictionary
    ):
        device_dictionary = model_to_dict(GoogleDeviceFactory.build(id="123456789"))
        mock__map_dictionary.return_value = device_dictionary
        sync_profile = GoogleDeviceSyncProfileFactory(
            name="staff", google_query="test_query"
        )
        sync_profile = GoogleDeviceSyncProfile.objects.get(name="staff")

        command = GoogleDevicesSyncCommand()
        # google_device doesn't matter since we are mocking the return of _map_dictionary
        return_value = command.convert_google_device_to_google_device(
            sync_profile=sync_profile, google_device={}
        )
        self.assertIsInstance(return_value, GoogleDevice)
        device = GoogleDevice(**device_dictionary)

        for field in [d.name for d in GoogleDevice._meta.concrete_fields]:
            self.assertEqual(getattr(device, field), getattr(return_value, field))

    def test_sync_google_devices(self):
        self.skipTest("Need to test")


class LinkGoogleDevicesTest(TestCase):
    def test_subclass(self):
        self.assertTrue(issubclass(GoogleDevicesLinkCommand, BaseCommand))

    def test_help(self):
        self.assertEqual(
            GoogleDevicesLinkCommand.help,
            "Associate imported device to their Google device counterpart.",
        )
