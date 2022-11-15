from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

from authentication.tests.decorators import assert_redirect_to_login
from inventory.tests.helpers import get_permission
from authentication.tests.factories import UserFactory
from .factories import DeviceAssignmentFactory
from people.tests.factories import PersonFactory
from devices.tests.factories import DeviceFactory
from assignments.models import DeviceAssignment
from assignments.views import DeviceAssignmentDatatableServerSideProcessingView
from django.core.exceptions import FieldError
import json
from unittest.mock import Mock, patch, ANY
from django.core.handlers.wsgi import WSGIRequest


class DeviceAssignmentListViewAuthenticatedWithPermissionTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        UserFactory(id=1)

    def setUp(self):
        self.user = User.objects.get(id=1)
        self.client.force_login(self.user)
        self.user.user_permissions.add(get_permission(DeviceAssignment, "view_deviceassignment"))

    def test_no_deviceassignments(self):
        response = self.client.get(reverse("assignments:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "assignments/deviceassignment_list.html")

    def test_one_deviceassignment(self):
        DeviceAssignmentFactory(id=1)
        response = self.client.get(reverse("assignments:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "assignments/deviceassignment_list.html")

    def test_ten_deviceassignments(self):
        DeviceAssignmentFactory.create_batch(10)
        response = self.client.get(reverse("assignments:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "assignments/deviceassignment_list.html")


class DeviceAssignmentDetailViewAuthenticatedWithPermissionTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        UserFactory(id=1)

    def setUp(self):
        self.user = User.objects.get(id=1)
        self.client.force_login(self.user)
        self.user.user_permissions.add(get_permission(DeviceAssignment, "view_deviceassignment"))

    def test_invalid_deviceassignment(self):
        response = self.client.get(reverse("assignments:detail", args=[1]))
        self.assertEqual(response.status_code, 404)

    def test_valid_deviceassignment(self):
        person = PersonFactory(first_name="TestName123")
        device = DeviceFactory(serial_number="TestSerial123", asset_id="TestAssetID123")
        device_assignment = DeviceAssignmentFactory(id=1, device=device, person=person)
        response = self.client.get(reverse("assignments:detail", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "assignments/partials/deviceassignment_auditlog.html")
        self.assertTemplateUsed(response, "assignments/deviceassignment_detail.html")
        self.assertContains(response, "TestName123")
        self.assertContains(response, "TestSerial123")
        self.assertContains(response, "TestAssetID123")
        self.assertEqual(response.context["deviceassignment"], device_assignment)


class DeviceAssignmentUpdateViewAuthenticatedWithPermissionTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        UserFactory(id=1)

    def setUp(self):
        self.user = User.objects.get(id=1)
        self.client.force_login(self.user)
        self.user.user_permissions.add(get_permission(DeviceAssignment, "change_deviceassignment"))

    def test_invalid_deviceassignment(self):
        response = self.client.get(reverse("assignments:edit", args=[1]))
        self.assertEqual(response.status_code, 404)

    def test_valid_deviceassignment(self):
        current_time = timezone.now()
        device_assignment = DeviceAssignmentFactory(id=1)
        response = self.client.get(reverse("assignments:edit", args=[1]))
        self.assertTemplateUsed(response, "assignments/deviceassignment_form.html")
        self.assertEqual(response.status_code, 200)


class DeviceAssignmentTurninViewAuthenticatedWithPermissionTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        UserFactory(id=1)

    def setUp(self):
        self.user = User.objects.get(id=1)
        self.client.force_login(self.user)
        self.user.user_permissions.add(get_permission(DeviceAssignment, "turnin_deviceassignment"))

    def test_invalid_deviceassignment(self):
        response = self.client.get(reverse("assignments:turnin", args=[1]))
        self.assertEqual(response.status_code, 404)

    def test_valid_deviceassignment(self):
        current_time = timezone.now()
        device_assignment = DeviceAssignmentFactory(id=1)
        response = self.client.get(reverse("assignments:turnin", args=[1]))
        self.assertTemplateUsed(response, "assignments/deviceassignment_turnin_form.html")
        self.assertEqual(response.status_code, 200)


class DeviceAssignmentCreateViewAuthenticatedWithPermissionTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        UserFactory(id=1)

    def setUp(self):
        self.user = User.objects.get(id=1)
        self.client.force_login(self.user)
        self.user.user_permissions.add(
            get_permission(DeviceAssignment, "add_deviceassignment"),
            get_permission(DeviceAssignment, "view_deviceassignment"),
        )

    def test_new_deviceassignment(self):
        response = self.client.get(reverse("assignments:new", args=[]))
        self.assertEqual(response.status_code, 200)

    def test_new_deviceassignment_post(self):

        device = DeviceFactory(id=1)
        person = PersonFactory(id=1)
        device_assignment_dict = {
            "device": device.id,
            "person": person.id,
        }
        response = self.client.post(reverse("assignments:new"), device_assignment_dict)
        device_assignment_object = DeviceAssignment.objects.last()
        self.assertIsNotNone(device_assignment_object)
        self.assertEqual(device_assignment_object.person, person)
        self.assertEqual(device_assignment_object.device, device)
        self.assertRedirects(
            response,
            reverse("assignments:detail", kwargs={"pk": device_assignment_object.pk}),
            status_code=302,
        )


class DeviceAssignmentDeleteViewAuthenticatedWithPermissionTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        UserFactory(id=1)
        DeviceAssignmentFactory(id=1)

    def setUp(self):
        self.user = User.objects.get(id=1)
        self.device_assignment = DeviceAssignment.objects.get(id=1)
        self.client.force_login(self.user)
        self.user.user_permissions.add(get_permission(DeviceAssignment, "delete_deviceassignment"))
        self.user.user_permissions.add(get_permission(DeviceAssignment, "view_deviceassignment"))

    def test_delete_deviceassignment(self):
        response = self.client.get(reverse("assignments:delete", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "assignments/deviceassignment_confirm_delete.html")

    def test_delete_deviceassignment_post(self):
        response = self.client.post(reverse("assignments:delete", args=[1]))
        self.assertRedirects(response, reverse("assignments:index"))
        device_assignments = DeviceAssignment.objects.filter(id=1)
        self.assertEqual(len(device_assignments), 0)


class DeviceAssignmentQuickAssignViewAuthenticatedWithPermissionTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        UserFactory(id=1)
        DeviceAssignmentFactory(id=1)

    def setUp(self):
        self.user = User.objects.get(id=1)
        self.device_assignment = DeviceAssignment.objects.get(id=1)
        self.client.force_login(self.user)
        self.user.user_permissions.add(get_permission(DeviceAssignment, "add_deviceassignment"))

    def test_quickassign_deviceassignment(self):
        response = self.client.get(reverse("assignments:quickassign"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "assignments/deviceassignment_quickassign.html")


class DeviceAssignmentDatatableServerSideProcessingViewAuthenticatedWithPermissionTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        UserFactory(id=1)
        DeviceAssignmentFactory(id=1)

    def setUp(self):
        self.user = User.objects.get(id=1)
        self.device_assignment = DeviceAssignment.objects.get(id=1)
        self.client.force_login(self.user)
        self.user.user_permissions.add(get_permission(DeviceAssignment, "view_deviceassignment"))

    def test_dt_index(self):
        response = self.client.get(reverse("assignments:dt_index"), self.get_dt_querydata())
        self.assertEqual(response.status_code, 200)

    def test_columns_defined_correctly(self):

        view = DeviceAssignmentDatatableServerSideProcessingView()
        self.assertTrue(isinstance(view.columns, list))
        try:
            returnable_values = view.queryset.values(*view.columns)
        except FieldError:
            self.fail("dt_index view specifies columns not accessible from the queryset!")
        # self.assertEqual(len(returnable_values[0].keys()], )

    @patch("assignments.views.render_to_string")
    def test_data_callback_adds_actions(self, mock_render_to_string):
        mock_render_to_string.return_value = "<div>mock_actions_html</div>"
        response = self.client.get(reverse("assignments:dt_index"), self.get_dt_querydata())
        json_data = json.loads(response.content)
        mock_render_to_string.assert_called_with(
            "assignments/partials/list/table_row_buttons.html",
            context=ANY,
            request=ANY,
        )
        args, kwargs = mock_render_to_string.call_args
        self.assertEqual(kwargs["context"]["deviceassignment"]["id"], 1)
        self.assertTrue(isinstance(kwargs["request"], WSGIRequest))
        self.assertEqual(
            json_data["data"][0]["actions"],
            mock_render_to_string.return_value,
            msg="actions field not set correctly!",
        )

    def get_dt_querydata(self):
        return {
            "draw": 1,
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
            "order[0][column]": 0,
            "order[0][dir]": "asc",
            "start": 0,
            "length": 10,
            "search[value]": "",
            "search[regex]": "false",
            "_": 1666386880919,
        }


class DeviceAssignmentViewsUnauthenticatedTest(TestCase):
    @assert_redirect_to_login(reverse("assignments:index"))
    def test_device_assignment_list_redirects_to_login(self):
        pass

    @assert_redirect_to_login(reverse("assignments:detail", args=[1]))
    def test_device_assignment_detail_redirects_to_login(self):
        pass

    @assert_redirect_to_login(reverse("assignments:edit", args=[1]))
    def test_device_assignment_update_redirects_to_login(self):
        pass

    @assert_redirect_to_login(reverse("assignments:turnin", args=[1]))
    def test_device_assignment_update_redirects_to_login(self):
        pass

    @assert_redirect_to_login(reverse("assignments:new"))
    def test_device_assignment_create_redirects_to_login(self):
        pass

    @assert_redirect_to_login(reverse("assignments:delete", args=[1]))
    def test_device_assignment_delete_redirects_to_login(self):
        pass

    @assert_redirect_to_login(reverse("assignments:quickassign"))
    def test_device_assignment_delete_redirects_to_login(self):
        pass

    @assert_redirect_to_login(reverse("assignments:quickassign_person_list"))
    def test_device_assignment_delete_redirects_to_login(self):
        pass

    @assert_redirect_to_login(reverse("assignments:quickassign_device_list"))
    def test_device_assignment_delete_redirects_to_login(self):
        pass

    @assert_redirect_to_login(reverse("assignments:quickassign_submit"))
    def test_device_assignment_delete_redirects_to_login(self):
        pass

    @assert_redirect_to_login(reverse("assignments:dt_index"))
    def test_device_assignment_dt_index_redirects_to_login(self):
        pass


class DeviceAssignmentViewsAuthenticatedWithoutPermissionTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        UserFactory(id=1)

    def setUp(self):
        self.user = User.objects.get(id=1)
        self.client.force_login(self.user)

    def test_device_assignment_list_redirects_to_login(self):
        response = self.client.get(reverse("assignments:index"))
        self.assertEqual(response.status_code, 403)

    def test_device_assignment_detail_redirects_to_login(self):
        response = self.client.get(reverse("assignments:detail", args=[1]))
        self.assertEqual(response.status_code, 403)

    def test_device_assignment_update_redirects_to_login(self):
        response = self.client.get(reverse("assignments:edit", args=[1]))
        self.assertEqual(response.status_code, 403)

    def test_device_assignment_create_redirects_to_login(self):
        response = self.client.get(reverse("assignments:new"))
        self.assertEqual(response.status_code, 403)

    def test_device_assignment_delete_redirects_to_login(self):
        response = self.client.get(reverse("assignments:delete", args=[1]))
        self.assertEqual(response.status_code, 403)

    def test_device_assignment_quickassign_redirect_to_login(self):
        response = self.client.get(reverse("assignments:quickassign"))
        self.assertEqual(response.status_code, 403)

    def test_device_assignment_quickassign_person_list_redirect_to_login(self):
        response = self.client.get(reverse("assignments:quickassign_person_list"))
        self.assertEqual(response.status_code, 403)

    def test_device_assignment_quickassign_person_list_redirect_to_login(self):
        response = self.client.get(reverse("assignments:quickassign_device_list"))
        self.assertEqual(response.status_code, 403)

    def test_device_assignment_quickassign_person_list_redirect_to_login(self):
        response = self.client.get(reverse("assignments:quickassign_submit"))
        self.assertEqual(response.status_code, 403)

    def test_device_assignment_dt_index_redirect_to_login(self):
        response = self.client.get(reverse("assignments:dt_index"))
        self.assertEqual(response.status_code, 403)
