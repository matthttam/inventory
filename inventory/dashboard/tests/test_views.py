from django.test import TestCase
from django.urls import reverse
from authentication.tests.factories import UserFactory
from django.contrib.auth.models import User
from authentication.tests.decorators import assert_redirect_to_login


class DeviceIndexViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        UserFactory(id=1)

    def setUp(self):
        user = User.objects.get(id=1)
        self.client.force_login(user)

    def test_index_view(self):
        response = self.client.get(reverse("dashboard:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/dashboard.html")
        self.assertTemplateUsed(response, "dashboard/dashboard_nav.html")
        self.assertTemplateUsed(response, "base.html")


class UnauthenticatedDeviceAssignmentViewTest(TestCase):
    @assert_redirect_to_login(reverse("dashboard:index"))
    def test_device_assignment_list_redirects_to_login(self):
        pass
