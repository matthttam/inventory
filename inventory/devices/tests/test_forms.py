from django.test import TestCase
from devices.forms import DeviceForm
from django.forms.models import model_to_dict
from devices.tests.factories import (
    DeviceFactory,
    DeviceModelFactory,
    DeviceStatusFactory,
)
from devices.models import DeviceModel, DeviceStatus
from locations.models import Building, Room


class DeviceFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        status = DeviceStatusFactory(name="test_status")
        device_model = DeviceModelFactory(id=1)

    def setUp(self):
        self.status = DeviceStatus.objects.get(name="test_status")
        self.device_model = DeviceModel.objects.get(id=1)

    def test_valid_form(self):
        device = DeviceFactory.build(status=self.status, device_model=self.device_model)
        form = DeviceForm(
            data=model_to_dict(
                device,
                fields=[
                    "serial_number",
                    "asset_id",
                    "device_model",
                    "status",
                    "building",
                    "room",
                    "notes",
                ],
            )
        )

        self.assertTrue(form.is_valid())
        self.assertEqual(form.errors, {})
        self.assertQuerysetEqual(
            form.fields["status"].queryset,
            DeviceStatus.objects.all(),
            ordered=False,
        )
        self.assertQuerysetEqual(
            form.fields["device_model"].queryset,
            DeviceModel.objects.all(),
            ordered=False,
        )
        self.assertQuerysetEqual(
            form.fields["building"].queryset,
            Building.objects.filter(active=True),
            ordered=False,
        )
        self.assertQuerysetEqual(
            form.fields["room"].queryset,
            Room.objects.filter(active=True),
            ordered=False,
        )

    def test_invalid_form(self):
        device = DeviceFactory(status=self.status, device_model=self.device_model)
        form = DeviceForm(
            data=model_to_dict(
                device,
                fields=[
                    "serial_number",
                    "asset_id",
                    "device_model",
                    "status",
                    "building",
                    "room",
                    "notes",
                ],
            )
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors.as_json(),
            '{"serial_number": [{"message": "Device with this Serial number already exists.", "code": "unique"}], "asset_id": [{"message": "Device with this Asset id already exists.", "code": "unique"}]}',
        )
