from django.test import TestCase
from devices.forms import DeviceForm
from django.forms.models import model_to_dict
from devices.tests.factories import (
    DeviceFactory,
    DeviceModelFactory,
    DeviceStatusFactory,
)
from devices.models import DeviceModel
from locations.models import Building, Room


# class DeviceFormTest(TestCase):
#    def test_valid_form(self):
#        status = DeviceStatusFactory()
#        device_model = DeviceModelFactory()
#        device = DeviceFactory.build(status=status, device_model=device_model)
#        form = DeviceForm(
#            data=model_to_dict(
#                device,
#                fields=[
#                    "serial_number",
#                    "asset_id",
#                    "device_model",
#                    "status",
#                    "building",
#                    "room",
#                    "notes",
#                ],
#            )
#        )
#
#        self.assertTrue(form.is_valid())
#        self.assertEqual(form.errors, {})
#        self.assertQuerysetEqual(
#            form.fields["device_model"].queryset,
#            DeviceModel.objects.all(),
#            ordered=False,
#        )
#        self.assertQuerysetEqual(
#            form.fields["building"].queryset,
#            Building.objects.filter(active=True),
#            ordered=False,
#        )
#        self.assertQuerysetEqual(
#            form.fields["room"].queryset,
#            Room.objects.filter(active=True),
#            ordered=False,
#        )
#
