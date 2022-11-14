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
from devices.views import DeviceDatatableServerSideProcessingView
from django.core.exceptions import FieldError
import json
from unittest.mock import Mock, patch, ANY, call
from django.core.handlers.wsgi import WSGIRequest
from callee import InstanceOf, String, Integer
from callee.collections import Dict
from callee.operators import Eq


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


class DeviceDatatableServerSideProcessingViewAuthenticatedWithPermissionTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        UserFactory(id=1)
        cls.device = DeviceFactory(id=1)

    def setUp(self):
        self.user = User.objects.get(id=1)
        self.device = Device.objects.get(id=1)
        self.client.force_login(self.user)
        self.user.user_permissions.add(get_permission(Device, "view_device"))

    def test_dt_index(self):
        response = self.client.get(reverse("devices:dt_index"), self.get_dt_querydata())
        self.assertEqual(response.status_code, 200)

    def test_columns_defined_correctly(self):

        view = DeviceDatatableServerSideProcessingView()
        self.assertTrue(isinstance(view.columns, list))
        try:
            returnable_values = view.queryset.values(*view.columns)
        except FieldError:
            self.fail("dt_index view specifies columns not accessible from the queryset!")

    @patch("devices.views.render_to_string")
    def test_data_callback_adds_actions(self, mock_render_to_string):
        actions_string = "<div>mock_actions_html</div>"
        check_string = "<div>mock_check</div>"
        mock_render_to_string.side_effect = [
            actions_string,
            check_string,
            check_string,
        ]
        response = self.client.get(reverse("devices:dt_index"), self.get_dt_querydata())
        json_data = json.loads(response.content)
        print(json_data)
        self.assertEqual(mock_render_to_string.call_count, 3)
        mock_render_to_string.assert_has_calls(
            [
                call(
                    "devices/partials/list/table_row_buttons.html",
                    context={"device": ANY},
                    request=InstanceOf(WSGIRequest),
                ),
                call(
                    "partials/check_or_x.html",
                    context={"boolean": ANY},
                    request=InstanceOf(WSGIRequest),
                ),
                call(
                    "partials/check_or_x.html",
                    context={"boolean": ANY},
                    request=InstanceOf(WSGIRequest),
                ),
            ],
            any_order=True,
        )

        self.assertEqual(
            json_data["data"][0]["actions"],
            actions_string,
            msg="actions field not set correctly!",
        )
        self.assertEqual(
            json_data["data"][0]["is_currently_assigned"],
            check_string,
            msg="is_currently_assigned field not set correctly!",
        )
        self.assertEqual(
            json_data["data"][0]["is_google_linked"],
            check_string,
            msg="is_google_linked field not set correctly!",
        )

    def get_dt_querydata(self):
        return {
            "draw": "1",
            "columns[0][data]": "id",
            "columns[0][name]": "",
            "columns[0][searchable]": "true",
            "columns[0][orderable]": "true",
            "columns[0][search][value]": "",
            "columns[0][search][regex]": "false",
            "columns[1][data]": "is_currently_assigned",
            "columns[1][name]": "",
            "columns[1][searchable]": "true",
            "columns[1][orderable]": "true",
            "columns[1][search][value]": "",
            "columns[1][search][regex]": "false",
            "columns[2][data]": "current_assignment_count",
            "columns[2][name]": "",
            "columns[2][searchable]": "true",
            "columns[2][orderable]": "true",
            "columns[2][search][value]": "",
            "columns[2][search][regex]": "false",
            "columns[3][data]": "asset_id",
            "columns[3][name]": "",
            "columns[3][searchable]": "true",
            "columns[3][orderable]": "true",
            "columns[3][search][value]": "",
            "columns[3][search][regex]": "false",
            "columns[4][data]": "serial_number",
            "columns[4][name]": "",
            "columns[4][searchable]": "true",
            "columns[4][orderable]": "true",
            "columns[4][search][value]": "",
            "columns[4][search][regex]": "false",
            "columns[5][data]": "status__name",
            "columns[5][name]": "",
            "columns[5][searchable]": "true",
            "columns[5][orderable]": "true",
            "columns[5][search][value]": "",
            "columns[5][search][regex]": "false",
            "columns[6][data]": "device_model__manufacturer__name",
            "columns[6][name]": "",
            "columns[6][searchable]": "true",
            "columns[6][orderable]": "true",
            "columns[6][search][value]": "",
            "columns[6][search][regex]": "false",
            "columns[7][data]": "device_model__name",
            "columns[7][name]": "",
            "columns[7][searchable]": "true",
            "columns[7][orderable]": "true",
            "columns[7][search][value]": "",
            "columns[7][search][regex]": "false",
            "columns[8][data]": "building__name",
            "columns[8][name]": "",
            "columns[8][searchable]": "true",
            "columns[8][orderable]": "true",
            "columns[8][search][value]": "",
            "columns[8][search][regex]": "false",
            "columns[9][data]": "is_google_linked",
            "columns[9][name]": "",
            "columns[9][searchable]": "false",
            "columns[9][orderable]": "true",
            "columns[9][search][value]": "",
            "columns[9][search][regex]": "false",
            "columns[10][data]": "google_device__organization_unit",
            "columns[10][name]": "",
            "columns[10][searchable]": "true",
            "columns[10][orderable]": "true",
            "columns[10][search][value]": "",
            "columns[10][search][regex]": "false",
            "columns[11][data]": "google_device__most_recent_user",
            "columns[11][name]": "",
            "columns[11][searchable]": "true",
            "columns[11][orderable]": "true",
            "columns[11][search][value]": "",
            "columns[11][search][regex]": "false",
            "columns[12][data]": "actions",
            "columns[12][name]": "",
            "columns[12][searchable]": "true",
            "columns[12][orderable]": "false",
            "columns[12][search][value]": "",
            "columns[12][search][regex]": "false",
            "order[0][column]": "0",
            "order[0][dir]": "asc",
            "start": "0",
            "length": "10",
            "search[value]": "",
            "search[regex]": "false",
            "_": "1666646122583",
        }


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

    @assert_redirect_to_login(reverse("devices:dt_index"))
    def test_device_dt_index_redirects_to_login(self):
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

    def test_device_dt_index_redirects_to_login(self):
        response = self.client.get(reverse("devices:dt_index"))
        self.assertEqual(response.status_code, 403)
