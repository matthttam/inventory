from django.test import TestCase
from django.urls import reverse
from .factories import DeviceAssignmentFactory
from people.tests.factories import PersonFactory
from devices.tests.factories import DeviceFactory
from assignments.models import DeviceAssignment
from django.utils import timezone
from authentication.tests.factories import UserFactory
from django.contrib.auth.models import User
from authentication.tests.decorators import assert_redirect_to_login


class DeviceAssignmentListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        UserFactory(id=1)

    def setUp(self):
        user = User.objects.get(id=1)
        self.client.force_login(user)

    def test_no_deviceassignments(self):
        response = self.client.get(reverse("assignments:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No assignments are available.")
        self.assertQuerysetEqual(response.context["object_list"], [])

    def test_one_deviceassignment(self):
        device_assignments = DeviceAssignmentFactory(id=1)
        response = self.client.get(reverse("assignments:index"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "No assignments are available.")
        self.assertQuerysetEqual(response.context["object_list"], [device_assignments])

    def test_ten_deviceassignments(self):
        device_assignments = DeviceAssignmentFactory.create_batch(10)
        response = self.client.get(reverse("assignments:index"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "No assignments are available.")
        self.assertQuerysetEqual(
            response.context["object_list"], device_assignments, ordered=False
        )


class DeviceAssignmentDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        UserFactory(id=1)

    def setUp(self):
        user = User.objects.get(id=1)
        self.client.force_login(user)

    def test_invalid_deviceassignment(self):
        response = self.client.get(reverse("assignments:detail", args=[1]))
        self.assertEqual(response.status_code, 404)

    def test_valid_deviceassignment(self):
        person = PersonFactory(first_name="TestName123")
        device = DeviceFactory(serial_number="TestSerial123", asset_id="TestAssetID123")
        device_assignment = DeviceAssignmentFactory(id=1, device=device, person=person)
        response = self.client.get(reverse("assignments:detail", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "TestName123")
        self.assertContains(response, "TestSerial123")
        self.assertContains(response, "TestAssetID123")
        self.assertEqual(response.context["deviceassignment"], device_assignment)


class DeviceAssignmentUpdateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        UserFactory(id=1)

    def setUp(self):
        user = User.objects.get(id=1)
        self.client.force_login(user)

    def test_invalid_deviceassignment(self):
        response = self.client.get(reverse("assignments:edit", args=[1]))
        self.assertEqual(response.status_code, 404)

    def test_valid_deviceassignment(self):
        current_time = timezone.now()
        device_assignment = DeviceAssignmentFactory(
            id=1, assignment_datetime=current_time
        )
        response = self.client.get(reverse("assignments:edit", args=[1]))
        self.assertEqual(response.status_code, 200)
        print(response.context)
        print(timezone.localtime(current_time).strftime("%Y-%m-%d %H:%M:%S"))


class DeviceAssignmentCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        UserFactory(id=1)

    def setUp(self):
        user = User.objects.get(id=1)
        self.client.force_login(user)

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


class UnauthenticatedDeviceAssignmentViewTest(TestCase):
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
