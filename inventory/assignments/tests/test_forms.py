from django.forms import model_to_dict
from django.test import TestCase
from assignments.forms import DeviceAssignmentForm
from people.models import Person
from devices.models import Device
from .factories import DeviceAssignmentFactory


class DeviceAssignmentFormTest(TestCase):
    def test_valid_form(self):
        device_assignment = DeviceAssignmentFactory()
        form = DeviceAssignmentForm(data=model_to_dict(device_assignment))
        self.assertTrue(form.is_valid())
        self.assertEqual(form.errors, {})
        self.assertQuerysetEqual(
            form.fields["device"].queryset,
            Device.objects.all(),
            ordered=False,
        )
        self.assertQuerysetEqual(
            form.fields["person"].queryset,
            Person.objects.filter(),
            ordered=False,
        )
