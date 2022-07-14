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
from authentication.tests.factories import UserFactory
from django.contrib.auth.models import User
from authentication.tests.decorators import assert_redirect_to_login


class DeviceListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        UserFactory(id=1)

    def setUp(self):
        user = User.objects.get(id=1)
        self.client.force_login(user)

    def test_no_devices(self):
        response = self.client.get(reverse("devices:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No devices are available.")
        self.assertQuerysetEqual(response.context["object_list"], [])

    def test_one_device(self):
        device = DeviceFactory(id=1)
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
    @classmethod
    def setUpTestData(cls):
        UserFactory(id=1)

    def setUp(self):
        user = User.objects.get(id=1)
        self.client.force_login(user)

    def test_invalid_device(self):
        response = self.client.get(reverse("devices:detail", args=[1]))
        self.assertEqual(response.status_code, 404)

    def test_valid_device(self):
        device = DeviceFactory(id=1, serial_number="ABCD1234")
        response = self.client.get(reverse("devices:detail", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ABCD1234")


class DeviceUpdateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        UserFactory(id=1)

    def setUp(self):
        user = User.objects.get(id=1)
        self.client.force_login(user)

    def test_invalid_device(self):
        response = self.client.get(reverse("devices:edit", args=[1]))
        self.assertEqual(response.status_code, 404)

    def test_valid_device(self):
        device = DeviceFactory(id=1)
        response = self.client.get(reverse("devices:edit", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, device.asset_id)


class DeviceCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        UserFactory(id=1)

    def setUp(self):
        user = User.objects.get(id=1)
        self.client.force_login(user)

    def test_new_device(self):
        response = self.client.get(reverse("devices:new", args=[]))
        self.assertEqual(response.status_code, 200)

    def test_new_device_post(self):
        device_status = DeviceStatusFactory(name="test_status")
        device_model = DeviceModelFactory(id=1)
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


class UnauthenticatedDeviceViewTest(TestCase):
    @assert_redirect_to_login(reverse("devices:index"))
    def test_device_list_redirects_to_login(self):
        pass

    @assert_redirect_to_login(reverse("devices:detail", args=[1]))
    def test_device_detail_redirects_to_login(self):
        pass

    @assert_redirect_to_login(reverse("devices:edit", args=[1]))
    def test_device_update_redirects_to_login(self):
        pass

    @assert_redirect_to_login(reverse("devices:new"))
    def test_device_create_redirects_to_login(self):
        pass
