from django.test import TestCase
from django.urls import reverse
from authentication.tests.factories import UserFactory
from django.contrib.auth.models import User
from authentication.tests.decorators import assert_redirect_to_login


class DashboardViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        UserFactory(id=1)

    def setUp(self):
        user = User.objects.get(id=1)
        self.client.force_login(user)

    def test_dashboard(self):
        response = self.client.get(reverse("dashboard:dashboard"))
        self.assertEqual(response.status_code, 200)


class UnauthenticatedDeviceAssignmentViewTest(TestCase):
    @assert_redirect_to_login(reverse("dashboard:dashboard"))
    def test_dashboard_redirects_to_login(self):
        pass
