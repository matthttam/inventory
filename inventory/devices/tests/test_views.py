from django.test import TestCase
from devices.models import DeviceStatus, DeviceManufacturer, Device, DeviceModel
from locations.models import Room, Building
from .factories import DeviceModelFactory, DeviceStatusFactory, DeviceManufacturerFactory, DeviceFactory
from django.urls import reverse


class DeviceListViewTest(TestCase):
    def test_no_devices(self):
        response = self.client.get(reverse("devices:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No devices are available.")
        self.assertQuerysetEqual(response.context['object_list'], [])

    def test_one_device(self):
        device = DeviceFactory()
        response = self.client.get(reverse("devices:index"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "No devices are available.")
        self.assertQuerysetEqual(response.context['object_list'], [device])

    def test_ten_devices(self):
        devices = [DeviceFactory()]
        response = self.client.get(reverse("devices:index"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "No devices are available.")
        self.assertQuerysetEqual(response.context['object_list'], [devices])


class DeviceDetailViewTest(TestCase):
    def test_invalid_device(self):
        response = self.client.get(
            reverse("devices:detail", args=[1]))
        self.assertEqual(response.status_code, 404)

    def test_valid_device(self):
        device = DeviceFactory(serial_number="ABCD1234")
        response = self.client.get(
            reverse("devices:detail", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ABCD1234")
    # def test_device_list_view

    # def test_device_detail
