from django.core.management.base import BaseCommand
from django.test import TestCase
from io import StringIO

from googlesync.management.commands._google_sync import GoogleSyncCommandAbstract
from googlesync.management.commands.update_google_devices import (
    Command as GoogleDevicesUpdateCommand,
)

from googlesync.models import (
    GoogleServiceAccountConfig,
)
from googlesync.tests.factories import (
    GoogleServiceAccountConfigFactory,
    GoogleDeviceFactory,
)
from devices.tests.factories import DeviceFactory
from locations.tests.factories import BuildingFactory
from assignments.tests.factories import (
    DeviceAssignmentFactory,
    DeviceAssignmentWithReturnDatetimeFactory,
)
from unittest.mock import patch, Mock, call
from people.tests.factories import PersonFactory, PersonTypeFactory


class UpdateGoogleDevicesTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        GoogleServiceAccountConfigFactory(project_id=1, delegate="test@example.com")

    def setUp(self):
        self.google_config = GoogleServiceAccountConfig.objects.get(project_id=1)

        # Mock the _get_my_customer call used in GoogleSyncCommand __init__
        self.mock_customer_resource = Mock(**{"get.return_value": "1234"})
        patcher__get_my_customer = patch.object(
            GoogleSyncCommandAbstract, "_get_my_customer"
        )

        self.addCleanup(patcher__get_my_customer.stop)
        self.mock__get_my_customer = patcher__get_my_customer.start()
        self.mock__get_my_customer.return_value = self.mock_customer_resource

    def test_subclass(self):
        self.assertTrue(issubclass(GoogleDevicesUpdateCommand, BaseCommand))

    def test_help(self):
        self.assertEqual(
            GoogleDevicesUpdateCommand.help,
            "Updates google device data based on assignment data",
        )

    @patch("sys.stdout", new_callable=StringIO)
    @patch.object(GoogleDevicesUpdateCommand, "_get_chromeosdevices_service")
    @patch.object(GoogleDevicesUpdateCommand, "get_devices_to_update")
    @patch.object(GoogleDevicesUpdateCommand, "get_chromeosdevices_patch_requests")
    @patch.object(GoogleDevicesUpdateCommand, "_process_batch_requests")
    @patch.object(GoogleDevicesUpdateCommand, "_patch_location_request_callback")
    def test_handle(
        self,
        mock__patch_location_request_callback,
        mock__process_batch_requests,
        mock_get_chromeosdevices_patch_requests,
        mock_get_devices_to_update,
        mock__get_chromeosdevices_service,
        mock_stdout,
    ):

        mock_devices = Mock()
        mock_get_devices_to_update.return_value = mock_devices
        mock_patch_request = Mock()
        mock_patch_requests = [mock_patch_request]
        mock_get_chromeosdevices_patch_requests.return_value = mock_patch_requests
        mock_chromeosdevices_service = Mock()
        mock__get_chromeosdevices_service.return_value = mock_chromeosdevices_service

        command = GoogleDevicesUpdateCommand()
        command.handle()

        mock__get_chromeosdevices_service.assert_called_once()
        mock_get_devices_to_update.assert_called_once()
        mock_get_chromeosdevices_patch_requests.assert_called_once_with(
            mock_chromeosdevices_service, mock_devices
        )
        mock_patch_request.execute.assert_called_once()
        # mock__process_batch_requests.assert_called_once_with(
        #    service=mock_chromeosdevices_service,
        #    requests=mock_patch_requests,
        #    callback=mock__patch_location_request_callback,
        # )
        self.assertEqual(mock_stdout.getvalue(), "Done\n")

    def test__patch_location_request_callback(self):
        self.skipTest("Need to test")

    def test_get_chromeosdevices_patch_requests(self):
        mock_patch1 = Mock()
        mock_patch2 = Mock()
        mock_patch3 = Mock()
        side_effect = [mock_patch1, mock_patch2, mock_patch3]
        mock_service = Mock(**{"patch.side_effect": side_effect})
        command = GoogleDevicesUpdateCommand()
        devices = [
            {
                "correct_google_location": "Building1,a@a.com",
                "current_google_location": None,
                "google_id": "40413525601230989101",
            },
            {
                "correct_google_location": "Building2,b@b.com",
                "current_google_location": None,
                "google_id": "40413525601230989102",
            },
            {
                "correct_google_location": "Building3,c@c.com",
                "current_google_location": None,
                "google_id": "40413525601230989103",
            },
        ]
        expected_calls = [
            call(
                customerId="1234",
                projection="FULL",
                deviceId="40413525601230989101",
                body={"annotatedLocation": "Building1,a@a.com"},
            ),
            call(
                customerId="1234",
                projection="FULL",
                deviceId="40413525601230989102",
                body={"annotatedLocation": "Building2,b@b.com"},
            ),
            call(
                customerId="1234",
                projection="FULL",
                deviceId="40413525601230989103",
                body={"annotatedLocation": "Building3,c@c.com"},
            ),
        ]
        command.get_chromeosdevices_patch_requests(mock_service, devices)
        print(mock_service.patch.call_args_list)
        self.assertCountEqual(mock_service.patch.call_args_list, expected_calls)

    def test_get_devices_to_update_uses_list_of_active_assigned_for_nonstaff(self):
        person_type_student = PersonTypeFactory(name="Student")
        person_type_staff = PersonTypeFactory(name="Staff")
        building1 = BuildingFactory(name="Building1")
        student_person = PersonFactory(
            type=person_type_student,
            email="a@a.com",
            primary_building=building1,
        )
        staff_person = PersonFactory(type=person_type_staff)
        google_device = GoogleDeviceFactory(
            serial_number="sn1",
            annotated_asset_id="asset1",
            location=None,
        )
        device = DeviceFactory(
            serial_number=google_device.serial_number,
            asset_id=google_device.annotated_asset_id,
            google_device=google_device,
        )
        DeviceAssignmentFactory(device=device, person=staff_person)
        DeviceAssignmentFactory(device=device, person=student_person)

        command = GoogleDevicesUpdateCommand()
        devices_to_update = command.get_devices_to_update()
        expected_results = [
            {
                "correct_google_location": f"Building1,{student_person.email}",
                "current_google_location": None,
                "google_id": google_device.id,
            }
        ]
        self.assertEqual(devices_to_update, expected_results)

        # Test it for multiple assignments
        building2 = BuildingFactory(name="Building2")
        student_person2 = PersonFactory(
            type=person_type_student, email="b@b.com", primary_building=building2
        )
        DeviceAssignmentFactory(device=device, person=student_person2)
        devices_to_update = command.get_devices_to_update()
        expected_results = [
            {
                "correct_google_location": f"Building2,{student_person.email},{student_person2.email}",
                "current_google_location": None,
                "google_id": google_device.id,
            }
        ]
        self.assertEqual(devices_to_update, expected_results)

    def test_get_devices_to_update_uses_star_for_unassigned(self):
        building1 = BuildingFactory(name="Building1")
        google_device = GoogleDeviceFactory(
            serial_number="sn1",
            annotated_asset_id="asset1",
            location=None,
        )
        DeviceFactory(
            serial_number=google_device.serial_number,
            asset_id=google_device.annotated_asset_id,
            building=building1,
            google_device=google_device,
        )

        command = GoogleDevicesUpdateCommand()
        devices_to_update = command.get_devices_to_update()
        expected_results = [
            {
                "correct_google_location": "Building1,*",
                "current_google_location": None,
                "google_id": google_device.id,
            }
        ]
        self.assertEqual(devices_to_update, expected_results)

    def test_get_devices_to_update_uses_star_for_staff(self):
        person_type_staff = PersonTypeFactory(name="Staff")
        building1 = BuildingFactory(name="Building1")
        staff_person = PersonFactory(type=person_type_staff, primary_building=building1)
        google_device = GoogleDeviceFactory(
            serial_number="sn1",
            annotated_asset_id="asset1",
            location=None,
        )
        staff_assigned_device = DeviceFactory(
            serial_number=google_device.serial_number,
            asset_id=google_device.annotated_asset_id,
            building=building1,
            google_device=google_device,
        )
        DeviceAssignmentFactory(device=staff_assigned_device, person=staff_person)

        command = GoogleDevicesUpdateCommand()
        devices_to_update = command.get_devices_to_update()
        expected_results = [
            {
                "correct_google_location": "Building1,*",
                "current_google_location": None,
                "google_id": google_device.id,
            }
        ]
        self.assertEqual(devices_to_update, expected_results)

    @patch.object(GoogleDevicesUpdateCommand, "_get_chromeosdevices_service")
    def test_move_google_device(self, mock__get_chromeosdevices_service):
        mock_response = Mock()
        mock_request = Mock(**{"execute.return_value": mock_response})
        mock_chromeosdevices_service = Mock(
            **{"moveDevicesToOu.return_value": mock_request}
        )
        mock__get_chromeosdevices_service.return_value = mock_chromeosdevices_service

        command = GoogleDevicesUpdateCommand()
        response = command.move_google_device("/org_unit", ["id1", "id2", "id3"])

        mock__get_chromeosdevices_service.assert_called_once()
        expected_options = {
            "customerId": "1234",
            "orgUnitPath": "/org_unit",
            "body": {"deviceIds": ["id1", "id2", "id3"]},
        }
        mock_chromeosdevices_service.moveDevicesToOu.assert_called_once_with(
            **expected_options
        )
        mock_request.execute.assert_called_once()
        self.assertEqual(response, mock_response)
