from django.test import TestCase
from django.urls import reverse
from authentication.tests.factories import UserFactory, SuperuserUserFactory
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from devices.models import Device
from people.models import Person
from assignments.models import DeviceAssignment
from inventory.tests.helpers import get_permission


class DashboardTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        SuperuserUserFactory(username="my_superuser@example.com")

    def setUp(self):
        self.user = User.objects.get(username="my_superuser@example.com")
        self.client.force_login(self.user)
        self.response = self.client.get(reverse("dashboard:dashboard"))

    def test_templates(self):
        self.assertTemplateUsed(self.response, "base.html")
        self.assertTemplateUsed(self.response, "dashboard/dashboard.html")
        self.assertTemplateUsed(self.response, "dashboard/partials/dashboard_nav.html")

    def test_title(self):
        self.assertInHTML("Inventory - Dashboard", self.response.content.decode())
