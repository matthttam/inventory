from django.test import TestCase
from django.urls import reverse
from .factories import DeviceAssignmentFactory
from people.tests.factories import PersonFactory
from devices.tests.factories import DeviceFactory


class DeviceAssignmentListViewTest(TestCase):
    def test_no_assignments(self):
        response = self.client.get(reverse("assignments:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No assignments are available.")
        self.assertQuerysetEqual(response.context["object_list"], [])

    def test_one_device(self):
        device_assignments = DeviceAssignmentFactory()
        response = self.client.get(reverse("assignments:index"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "No assignments are available.")
        self.assertQuerysetEqual(response.context["object_list"], [device_assignments])

    def test_ten_devices(self):
        device_assignments = DeviceAssignmentFactory.create_batch(10)
        response = self.client.get(reverse("assignments:index"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "No assignments are available.")
        self.assertQuerysetEqual(
            response.context["object_list"], device_assignments, ordered=False
        )


class DeviceAssignmentDetailViewTest(TestCase):
    def test_invalid_device(self):
        response = self.client.get(reverse("assignments:detail", args=[1]))
        self.assertEqual(response.status_code, 404)

    def test_valid_device(self):
        person = PersonFactory(first_name="TestName123")
        device = DeviceFactory(serial_number="TestSerial123", asset_id="TestAssetID123")
        DeviceAssignmentFactory(device=device, person=person)
        response = self.client.get(reverse("assignments:detail", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "TestName123")
        self.assertContains(response, "TestSerial123")
        self.assertContains(response, "TestAssetID123")
