from datetime import datetime
from unittest.mock import patch
from zoneinfo import ZoneInfo

from assignments.models import DeviceAssignment
from assignments.tests.factories import DeviceAssignmentFactory
from devices.signals import device_assignment_creation_action, device_turnin_action
from devices.tests.factories import DeviceFactory
from django.test import TestCase
from googlesync.tests.factories import (
    DeviceBuildingToGoogleOUMappingFactory,
    GoogleDeviceFactory,
    GoogleDeviceMappingFactory,
)
from locations.tests.factories import BuildingFactory
from people.tests.factories import PersonFactory


class AssignmentActions(TestCase):
    def test_device_assignment_creation_google_device_calls_device_assignment_creation_action(
        self,
    ):
        with patch(
            "devices.signals.device_assignment_creation_action"
        ) as mock_create_function:
            with patch("devices.signals.device_turnin_action") as mock_turnin_function:
                google_device = GoogleDeviceFactory()
                device = DeviceFactory(google_device=google_device)
                person = PersonFactory()
                assignment = DeviceAssignmentFactory(
                    device=device, person=person, return_datetime=None
                )
                self.assertTrue(mock_create_function.called)
                self.assertEqual(mock_create_function.call_count, 1)
                self.assertTrue(mock_create_function.called_with(person, device))

                self.assertFalse(mock_turnin_function.called)

    @patch("devices.signals.device_assignment_creation_action")
    @patch("devices.signals.device_turnin_action")
    def test_device_assignment_creation_non_google_device_calls_no_action(
        self, mock_create_function, mock_turnin_function
    ):
        device = DeviceFactory(google_device=None)
        person = PersonFactory()
        assignment = DeviceAssignmentFactory(device=device, person=person)

        self.assertFalse(mock_turnin_function.called)
        self.assertFalse(mock_create_function.called)

    def test_device_assignment_save_updates_device_building(self):
        building_a = BuildingFactory(name="A")
        building_b = BuildingFactory(name="B")
        device = DeviceFactory(building=building_a)
        person = PersonFactory(primary_building=building_b)
        self.assertNotEqual(device.building, person.primary_building)
        DeviceAssignmentFactory(device=device, person=person)
        self.assertEqual(device.building, person.primary_building)

    def test_device_assignment_create_with_no_primary_building_does_not_update_device(
        self,
    ):
        building_a = BuildingFactory(name="A")
        device = DeviceFactory(building=building_a)
        person = PersonFactory(primary_building=None)
        self.assertNotEqual(device.building, person.primary_building)
        DeviceAssignmentFactory(device=device, person=person)
        self.assertNotEqual(device.building, person.primary_building)

    def test_device_assignment_turnin_calls_device_turnin_action(self):
        google_device = GoogleDeviceFactory()
        device = DeviceFactory(google_device=google_device)
        person = PersonFactory()
        assignment = DeviceAssignmentFactory(
            device=device, person=person, return_datetime=None
        )
        with patch(
            "devices.signals.device_assignment_creation_action"
        ) as mock_create_function:
            with patch("devices.signals.device_turnin_action") as mock_turnin_action:
                assignment = DeviceAssignment.objects.filter(device=device).first()
                tz = ZoneInfo(key="America/Chicago")
                assignment.return_datetime = datetime.now(tz=tz)
                assignment.save()
                self.assertTrue(mock_turnin_action.called)
                self.assertEqual(mock_turnin_action.call_count, 1)
                self.assertTrue(mock_turnin_action.called_with(person, device))
                self.assertFalse(mock_create_function.called)


class AssignmentCreationAction(TestCase):
    @patch("devices.signals.change_device_ou")
    def test_no_mapping_does_nothing(self, mock_change_device_ou):
        person = PersonFactory()
        device = DeviceFactory()
        device_assignment_creation_action(person, device)
        self.assertFalse(mock_change_device_ou.called)

    @patch("devices.signals.change_device_ou")
    def test_valid_mapping_calls_change_device_ou(self, mock_change_device_ou):
        new_ou = "/new_value/test"
        old_ou = "/"
        mapping = DeviceBuildingToGoogleOUMappingFactory(organization_unit=new_ou)
        person = PersonFactory(primary_building=mapping.building)
        google_device = GoogleDeviceFactory(organization_unit=old_ou)
        device = DeviceFactory(google_device=google_device)
        DeviceAssignmentFactory(device=device, person=person)
        self.assertTrue(mock_change_device_ou.called)
        self.assertTrue(mock_change_device_ou.call_count, 1)
        self.assertTrue(mock_change_device_ou.called_with(new_ou, device))
        # self.assertEqual(device.google_device.organization_unit, new_ou)


class AssignmentTurninAction(TestCase):
    def test_device_assignment_actions(self):
        self.skipTest("Need to implement")

    def test_device_assignment_actions(self):
        self.skipTest("Need to implement")

    def test_device_assignment_creation_action(self):
        self.skipTest("Need to implement")

    def test_device_turnin_action(self):
        self.skipTest("Need to implement")
