from zoneinfo import ZoneInfo
from datetime import datetime
from unittest.mock import patch

from django.test import TestCase
from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from django.db.models.signals import post_save
from assignments.models import (
    AssignmentAbstract,
    DeviceAssignment,
    DeviceAccessoryAssignment,
    AssignmentManager,
)
from locations.tests.factories import BuildingFactory
from people.models import Person
from devices.models import Device, DeviceAccessory
from devices.tests.factories import DeviceFactory
from people.tests.factories import PersonFactory
from assignments.forms import DeviceAssignmentForm

from .factories import DeviceAssignmentFactory, DeviceAccessoryAssignmentFactory
from people.tests.factories import PersonFactory


# Test the abstract assignment class
class AssignmentAbstractTest(TestCase):
    def test_is_abstract(self):
        self.assertTrue(AssignmentAbstract._meta.abstract)

    def test_assignment_datetime_label(self):
        field_label = AssignmentAbstract._meta.get_field(
            "assignment_datetime"
        ).verbose_name
        self.assertEqual(field_label, "assignment date")

    def test_assignment_datetime_auto_now(self):
        self.assertTrue(
            AssignmentAbstract._meta.get_field("assignment_datetime").auto_now_add
        )

    def test_return_datetime_label(self):
        field_label = AssignmentAbstract._meta.get_field("return_datetime").verbose_name
        self.assertEqual(field_label, "return date")

    def test_return_datetime_default(self):
        default = AssignmentAbstract._meta.get_field("return_datetime").default
        self.assertIsNone(default)

    def test_return_datetime_null(self):
        null = AssignmentAbstract._meta.get_field("return_datetime").null
        self.assertTrue(null)

    def test_objects_is_instance_of_assignment_manager(self):
        self.assertIsInstance(AssignmentAbstract._default_manager, AssignmentManager)

    ### Functions ###
    # @patch("assignments.models.AssignmentAbstract._meta.abstract", set())
    # def test_is_outstanding(self):


#
#    assignment = AssignmentAbstract(
#        assignment_datetime=datetime(
#            2022, 5, 30, 15, 44, 47, tzinfo=ZoneInfo(key="America/Chicago")
#        ),
#        return_datetime=None,
#    )
#    self.assertEqual(
#        assignment.is_outstanding,
#        True,
#    )
#    assignment.return_datetime = assignment.assignment_datetime
#    self.assertEqual(
#        assignment.is_outstanding,
#        False,
#    )
#


class DeviceAssignmentTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        DeviceAssignmentFactory(id=1)

    def setUp(self):
        self.device_assignment = DeviceAssignment.objects.get(id=1)

    def test_subclass(self):
        self.assertTrue(issubclass(DeviceAssignment, AssignmentAbstract))

    def test_device_foreign_key(self):
        self.assertEqual(
            self.device_assignment._meta.get_field("device").related_model, Device
        )

    def test_history_class(self):
        self.assertIsInstance(
            DeviceAssignment._meta.get_field("history"), AuditlogHistoryField
        )

    def test_person_foreign_key(self):
        self.assertEqual(
            DeviceAssignment._meta.get_field("person").related_model, Person
        )

    def test_person_related_name(self):
        self.assertEqual(
            DeviceAssignment._meta.get_field("person")._related_name,
            "deviceassignments",
        )

    ### Functions ###
    def test_get_absolute_url(self):
        self.assertEqual(self.device_assignment.get_absolute_url(), "/assignments/1/")

    def test_auditlog_register(self):
        self.assertTrue(auditlog.contains(model=DeviceAssignment))


class DeviceAccessoryAssignmentTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        DeviceAccessoryAssignmentFactory(id=1)

    def setUp(self):
        self.device_accessory_assignment = DeviceAccessoryAssignment.objects.get(id=1)

    def test_subclass(self):
        self.assertTrue(issubclass(DeviceAssignment, AssignmentAbstract))

    def test_device_foreign_key(self):
        self.assertEqual(
            self.device_accessory_assignment._meta.get_field(
                "device_accessory"
            ).related_model,
            DeviceAccessory,
        )

    def test_person_foreign_key(self):
        self.assertEqual(
            self.device_accessory_assignment._meta.get_field("person").related_model,
            Person,
        )

    def test_person_related_name(self):
        print(dir(self.device_accessory_assignment._meta.get_field("person")))
        self.assertEqual(
            self.device_accessory_assignment._meta.get_field("person")._related_name,
            "deviceaccessoryassignments",
        )
