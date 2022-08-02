from django.core.management.base import BaseCommand
from django.test import TestCase
from parameterized import parameterized
from django.core.management import call_command

from googlesync.management.commands._google_sync import GoogleSyncCommandAbstract
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


class SyncGoogleDevicesTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        GoogleServiceAccountConfigFactory(project_id=1, delegate="test@example.com")

    def setUp(self):
        self.google_config = GoogleServiceAccountConfig.objects.get(project_id=1)

        # Mock the _get_my_customer call used in GoogleSyncCommand __init__
        mock_customer_resource = Mock()
        patcher__get_my_customer = patch.object(
            GoogleSyncCommandAbstract, "_get_my_customer"
        )

        self.addCleanup(patcher__get_my_customer.stop)
        self.mock__get_my_customer = patcher__get_my_customer.start()
        self.mock__get_my_customer.return_value = mock_customer_resource

    def test_subclass(self):
        self.assertTrue(issubclass(GoogleDevicesSyncCommand, GoogleSyncCommandAbstract))

    def test_help(self):
        self.assertEqual(
            GoogleDevicesSyncCommand.help, "Syncs google devices to inventory devices."
        )

    def test__sync_google_device_profiles(self):
        self.skipTest("Need to test")

    def test__sync_google_device_profile(self):
        self.skipTest("Need to test")

    def test__initilaize_device_sync(self):
        self.skipTest("Need to test")

    @patch.object(GoogleDevicesSyncCommand, "sync_google_devices")
    def test__get_device_sync_profile_invalid_names(self, mock_sync_google_devices):
        with self.assertRaises(SyncProfileNotFound) as context:
            call_command("sync_google_devices", "sync", "random_profile")
        self.assertEqual(str(context.exception), "'random_profile' profile not found")

        GoogleDeviceSyncProfileFactory(name="real_sync_profile")
        with self.assertRaises(SyncProfileNotFound) as context:
            call_command(
                "sync_google_devices", "sync", "real_sync_profile", "fake_sync_profile"
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

        call_command("sync_google_devices", "sync", "real_sync_profile")

        mock_sync_google_devices.assert_called_with(google_device_sync1)
        mock_sync_google_devices.asssert_not_called_with(google_device_sync2)

        mock_sync_google_devices.reset_mock()
        call_command(
            "sync_google_devices",
            "sync",
            "real_sync_profile",
            "another_real_sync_profile",
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
