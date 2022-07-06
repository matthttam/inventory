from django.forms import model_to_dict
from django.test import TestCase
from devices.models import DeviceStatus, DeviceManufacturer, Device, DeviceModel
from googlesync.tests.factories import GoogleDeviceFactory
from locations.models import Room, Building
from .factories import (
    DeviceModelFactory,
    DeviceStatusFactory,
    DeviceManufacturerFactory,
    DeviceFactory,
)
from django.urls import reverse
from django.forms import model_to_dict


class DeviceListViewTest(TestCase):
    def test_no_devices(self):
        response = self.client.get(reverse("devices:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No devices are available.")
        self.assertQuerysetEqual(response.context["object_list"], [])

    def test_one_device(self):
        device = DeviceFactory()
        response = self.client.get(reverse("devices:index"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "No devices are available.")
        self.assertQuerysetEqual(response.context["object_list"], [device])

    def test_ten_devices(self):
        devices = DeviceFactory.create_batch(10)
        response = self.client.get(reverse("devices:index"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "No devices are available.")
        self.assertQuerysetEqual(
            response.context["object_list"], devices, ordered=False
        )


class DeviceDetailViewTest(TestCase):
    def test_invalid_device(self):
        response = self.client.get(reverse("devices:detail", args=[1]))
        self.assertEqual(response.status_code, 404)

    def test_valid_device(self):
        device = DeviceFactory(serial_number="ABCD1234")
        response = self.client.get(reverse("devices:detail", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ABCD1234")


class DeviceUpdateViewTest(TestCase):
    def test_invalid_device(self):
        response = self.client.get(reverse("devices:edit", args=[1]))
        self.assertEqual(response.status_code, 404)

    def test_valid_device(self):
        device = DeviceFactory()
        response = self.client.get(reverse("devices:edit", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, device.asset_id)


class DeviceCreateViewTest(TestCase):
    def test_new_device(self):
        response = self.client.get(reverse("devices:new", args=[]))
        self.assertEqual(response.status_code, 200)

    def test_new_device_post(self):
        device_status = DeviceStatusFactory()
        device_model = DeviceModelFactory()
        google_device = GoogleDeviceFactory
        device_dict = {
            "serial_number": "SN-18",
            "asset_id": "ASSET-18",
            "notes": "",
            "status": device_status.id,
            "device_model": device_model.id,
            "google_device": google_device.id,
            "building": "",
            "room": "",
        }
        response = self.client.post(reverse("devices:new"), device_dict)
        device_object = Device.objects.last()
        self.assertIsNotNone(device_object)
        self.assertEqual(device_object.serial_number, device_dict["serial_number"])
        self.assertRedirects(
            response,
            reverse("devices:detail", kwargs={"pk": device_object.pk}),
            status_code=302,
        )
