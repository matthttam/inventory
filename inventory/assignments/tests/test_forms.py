from django.forms import model_to_dict
from django.test import TestCase
from people.tests.factories import PersonFactory
from devices.tests.factories import DeviceFactory
from assignments.forms import DeviceAssignmentForm
from people.models import Person
from devices.models import Device
from .factories import DeviceAssignmentFactory


class DeviceAssignmentFormTest(TestCase):
    def test_valid_form(self):
        person = PersonFactory()
        device = DeviceFactory()
        device_assignment = DeviceAssignmentFactory()
        form = DeviceAssignmentForm(data=model_to_dict(Device))
        self.assertTrue(form.is_valid())
        self.assertEqual(form.errors, {})
        self.assertQuerysetEqual(
            form.fields["device"].queryset,
            Device.objects.all(),
            ordered=False,
        )
        self.assertQuerysetEqual(
            form.fields["person"].queryset,
            Person.objects.filter(active=True),
            ordered=False,
        )
        self.assertQuerysetEqual(
            form.fields["room"].queryset,
            Room.objects.filter(active=True),
            ordered=False,
        )
