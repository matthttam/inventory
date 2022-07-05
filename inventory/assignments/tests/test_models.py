from django.test import TestCase
from assignments.models import Assignment, DeviceAssignment, DeviceAccessoryAssignment
from people.models import Person
from devices.models import Device, DeviceAccessory
from .factories import DeviceAssignmentFactory, DeviceAccessoryAssignmentFactory

# Test the abstract assignment class
class AssignmentTest(TestCase):
    def test_is_abstract(self):
        self.assertTrue(Assignment._meta.abstract)

    def test_datetime_label(self):
        field_label = Assignment._meta.get_field("assignment_datetime").verbose_name
        self.assertEqual(field_label, "assignment date")

    def test_return_datetime_label(self):
        field_label = Assignment._meta.get_field("return_datetime").verbose_name
        self.assertEqual(field_label, "return date")

    def test_return_datetime_default(self):
        default = Assignment._meta.get_field("return_datetime").default
        self.assertIsNone(default)

    def test_return_datetime_null(self):
        null = Assignment._meta.get_field("return_datetime").null
        self.assertTrue(null)

    def test_person_foreign_key(self):
        self.assertEqual(Assignment._meta.get_field("person").related_model, Person)


class DeviceAssignmentTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        DeviceAssignmentFactory()

    def setUp(self):
        self.device_assignment = DeviceAssignment.objects.get(id=1)

    def test_subclass(self):
        self.assertTrue(issubclass(DeviceAssignment, Assignment))

    def test_device_foreign_key(self):
        self.assertEqual(
            self.device_assignment._meta.get_field("device").related_model, Device
        )

    ### Functions ###
    def test_get_absolute_url(self):
        self.assertEqual(self.device_assignment.get_absolute_url(), "/assignments/1/")


class DeviceAccessoryAssignmentTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        DeviceAccessoryAssignmentFactory()

    def setUp(self):
        self.device_accessory_assignment = DeviceAccessoryAssignment.objects.get(id=1)

    def test_subclass(self):
        self.assertTrue(issubclass(DeviceAssignment, Assignment))

    def test_device_foreign_key(self):
        self.assertEqual(
            self.device_accessory_assignment._meta.get_field(
                "device_accessory"
            ).related_model,
            DeviceAccessory,
        )