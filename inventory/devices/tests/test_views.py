from django.forms import model_to_dict
from django.test import TestCase
from devices.models import DeviceStatus, DeviceManufacturer, Device, DeviceModel
from googlesync.tests.factories import GoogleDeviceFactory
from locations.models import Room, Building
from .factories import (
    DeviceModelFactory,
    DeviceStatusFactory,
    DeviceFactory,
)
from django.urls import reverse
from django.forms import model_to_dict
from authentication.tests.factories import UserFactory
from django.contrib.auth.models import User
from authentication.tests.decorators import assert_redirect_to_login
from inventory.tests.helpers import get_permission


class DeviceListViewAuthenticatedWithPermissionTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        UserFactory(id=1)

    def setUp(self):
        self.user = User.objects.get(id=1)
        self.client.force_login(self.user)
        self.user.user_permissions.add(get_permission(Device, "view_device"))

    def test_no_devices(self):
        response = self.client.get(reverse("devices:index"))
        self.assertEqual(response.status_code, 200)

    def test_one_device(self):
        device = DeviceFactory(id=1)
        response = self.client.get(reverse("devices:index"))
        self.assertEqual(response.status_code, 200)

    def test_ten_devices(self):
        devices = DeviceFactory.create_batch(10)
        response = self.client.get(reverse("devices:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "devices/device_list.html")


class DeviceDetailViewAuthenticatedWithPermissionTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        UserFactory(id=1)

    def setUp(self):
        self.user = User.objects.get(id=1)
        self.client.force_login(self.user)
        self.user.user_permissions.add(get_permission(Device, "view_device"))

    def test_invalid_device(self):
        response = self.client.get(reverse("devices:detail", args=[1]))
        self.assertEqual(response.status_code, 404)

    def test_valid_device(self):
        device = DeviceFactory(id=1, serial_number="ABCD1234")
        response = self.client.get(reverse("devices:detail", args=[1]))
        self.assertTemplateUsed(response, "devices/device_detail.html")
        self.assertTemplateUsed(
            response, "devices/partials/device_detail/tab_device_detail.html"
        )
        self.assertTemplateUsed(
            response, "devices/partials/device_detail/tab_device_history.html"
        )
        self.assertTemplateUsed(
            response, "devices/partials/device_detail/tab_assignment_history.html"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ABCD1234")


class DeviceUpdateViewAuthenticatedWithPermissionTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        UserFactory(id=1)

    def setUp(self):
        self.user = User.objects.get(id=1)
        self.client.force_login(self.user)
        self.user.user_permissions.add(get_permission(Device, "change_device"))

    def test_invalid_device(self):
        response = self.client.get(reverse("devices:edit", args=[1]))
        self.assertEqual(response.status_code, 404)

    def test_valid_device(self):
        device = DeviceFactory(id=1)
        response = self.client.get(reverse("devices:edit", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, device.asset_id)


class DeviceCreateViewAuthenticatedWithPermissionTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        UserFactory(id=1)

    def setUp(self):
        self.user = User.objects.get(id=1)
        self.client.force_login(self.user)
        self.user.user_permissions.add(
            get_permission(Device, "add_device"),
            get_permission(Device, "view_device"),
        )

    def test_new_device(self):
        response = self.client.get(reverse("devices:new", args=[]))
        self.assertEqual(response.status_code, 200)

    def test_new_device_post(self):
        device_status = DeviceStatusFactory(name="test_status")
        device_model = DeviceModelFactory(id=1)
        google_device = GoogleDeviceFactory()
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


class DeviceDeleteViewAuthenticatedWithPermissionTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        UserFactory(id=1)
        DeviceFactory(id=1)

    def setUp(self):
        self.user = User.objects.get(id=1)
        self.device = Device.objects.get(id=1)
        self.client.force_login(self.user)
        self.user.user_permissions.add(
            get_permission(Device, "delete_device"),
            get_permission(Device, "view_device"),
        )

    def test_delete_device(self):
        response = self.client.get(reverse("devices:delete", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "devices/device_confirm_delete.html")

    def test_delete_device_post(self):
        response = self.client.post(reverse("devices:delete", args=[1]))
        self.assertRedirects(response, reverse("devices:index"))
        devices = Device.objects.filter(id=1)
        self.assertEqual(len(devices), 0)


class DeviceViewUnauthenticatedTest(TestCase):
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

    @assert_redirect_to_login(reverse("devices:delete", args=[1]))
    def test_device_delete_redirects_to_login(self):
        pass


class DeviceViewsAuthenticatedWithoutPermissionTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        UserFactory(id=1)

    def setUp(self):
        self.user = User.objects.get(id=1)
        self.client.force_login(self.user)

    def test_device_list_redirects_to_login(self):
        response = self.client.get(reverse("devices:index"))
        self.assertEqual(response.status_code, 403)

    def test_device_detail_redirects_to_login(self):
        response = self.client.get(reverse("devices:detail", args=[1]))
        self.assertEqual(response.status_code, 403)

    def test_device_update_redirects_to_login(self):
        response = self.client.get(reverse("devices:edit", args=[1]))
        self.assertEqual(response.status_code, 403)

    def test_device_create_redirects_to_login(self):
        response = self.client.get(reverse("devices:new"))
        self.assertEqual(response.status_code, 403)

    def test_device_delete_redirects_to_login(self):
        response = self.client.get(reverse("devices:delete", args=[1]))
        self.assertEqual(response.status_code, 403)
