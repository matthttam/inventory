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


class DeviceAssignmentListViewAuthenticatedWithPermissionTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        UserFactory(id=1)

    def setUp(self):
        self.user = User.objects.get(id=1)
        self.client.force_login(self.user)
        self.user.user_permissions.add(
            get_permission(DeviceAssignment, "view_deviceassignment")
        )

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
        self.user.user_permissions.add(
            get_permission(DeviceAssignment, "view_deviceassignment")
        )

    def test_invalid_deviceassignment(self):
        response = self.client.get(reverse("assignments:detail", args=[1]))
        self.assertEqual(response.status_code, 404)

    def test_valid_deviceassignment(self):
        person = PersonFactory(first_name="TestName123")
        device = DeviceFactory(serial_number="TestSerial123", asset_id="TestAssetID123")
        device_assignment = DeviceAssignmentFactory(id=1, device=device, person=person)
        response = self.client.get(reverse("assignments:detail", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "assignments/partials/deviceassignment_auditlog.html"
        )
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
        self.user.user_permissions.add(
            get_permission(DeviceAssignment, "change_deviceassignment")
        )

    def test_invalid_deviceassignment(self):
        response = self.client.get(reverse("assignments:edit", args=[1]))
        self.assertEqual(response.status_code, 404)

    def test_valid_deviceassignment(self):
        current_time = timezone.now()
        device_assignment = DeviceAssignmentFactory(id=1)
        response = self.client.get(reverse("assignments:edit", args=[1]))
        self.assertTemplateUsed(response, "assignments/deviceassignment_form.html")
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
        self.user.user_permissions.add(
            get_permission(DeviceAssignment, "delete_deviceassignment")
        )
        self.user.user_permissions.add(
            get_permission(DeviceAssignment, "view_deviceassignment")
        )

    def test_delete_deviceassignment(self):
        response = self.client.get(reverse("assignments:delete", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "assignments/deviceassignment_confirm_delete.html"
        )

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
        self.user.user_permissions.add(
            get_permission(DeviceAssignment, "add_deviceassignment")
        )

    def test_quickassign_deviceassignment(self):
        response = self.client.get(reverse("assignments:quickassign"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "assignments/deviceassignment_quickassign.html"
        )


class DeviceAssignmentViewUnauthenticatedTest(TestCase):
    @assert_redirect_to_login(reverse("assignments:index"))
    def test_device_assignment_list_redirects_to_login(self):
        pass

    @assert_redirect_to_login(reverse("assignments:detail", args=[1]))
    def test_device_assignment_detail_redirects_to_login(self):
        pass

    @assert_redirect_to_login(reverse("assignments:edit", args=[1]))
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
