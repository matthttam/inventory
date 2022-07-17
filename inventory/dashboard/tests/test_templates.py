from django.test import TestCase
from django.urls import reverse
from authentication.tests.factories import UserFactory, SuperuserUserFactory
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from devices.models import Device
from people.models import Person
from assignments.models import DeviceAssignment
from inventory.tests.helpers import get_permission

# Links that may appear on dashboard

dashboard_link = '<a class="nav-link active" aria-current="page" href="/">Dashboard</a>'
devices_link = '<a class="nav-link " aria-current="page" href="/devices/">Devices</a>'
people_link = '<a class="nav-link " aria-current="page" href="/people/">People</a>'
assignments_link = (
    '<a class="nav-link " aria-current="page" href="/assignments/">Assignments</a>'
)
google_sync_link = '<a class="nav-link " aria-current="page" href="">Google Sync</a>'


# Links all users should have access to
DEFAULT_LINKS = [dashboard_link]


class DashboardNavTestSuperuserUser(TestCase):
    """Checks that the dashboard template loads the appropriate links for a superuser."""

    @classmethod
    def setUpTestData(cls):
        SuperuserUserFactory(username="my_superuser@example.com")

    def setUp(self):
        user = User.objects.get(username="my_superuser@example.com")
        self.client.force_login(user)
        self.response = self.client.get(reverse("dashboard:index"))

    def test_default_links_exist(self):
        for link in DEFAULT_LINKS:
            self.assertInHTML(
                link,
                self.response.content.decode(),
            )

    def test_all_links_exist(self):
        links = [
            devices_link,
            people_link,
            assignments_link,
            google_sync_link,
        ]
        for link in links:
            self.assertInHTML(
                link,
                self.response.content.decode(),
            )


class DashboardNavTestRegularUser(TestCase):
    """Test a base user type with basic permissions on dashboard"""

    @classmethod
    def setUpTestData(cls):
        UserFactory(username="my_regularuser@example.com")

    def setUp(self):
        self.user = User.objects.get(username="my_regularuser@example.com")
        self.client.force_login(self.user)

    def test_google_sync_missing(self):
        self.response = self.client.get(reverse("dashboard:index"))
        self.assertNotIn(
            google_sync_link,
            self.response.content.decode(),
        )

    def test_devices_requires_device_view_permission(self):
        self.response = self.client.get(reverse("dashboard:index"))
        self.assertNotIn(
            devices_link,
            self.response.content.decode(),
        )
        self.user.user_permissions.add(get_permission(Device, "view_device"))
        self.response = self.client.get(reverse("dashboard:index"))
        self.assertIn(
            devices_link,
            self.response.content.decode(),
        )

    def test_people_requires_person_view_permission(self):
        self.response = self.client.get(reverse("dashboard:index"))
        self.assertNotIn(
            people_link,
            self.response.content.decode(),
        )
        self.user.user_permissions.add(get_permission(Person, "view_person"))
        self.response = self.client.get(reverse("dashboard:index"))
        self.assertIn(
            people_link,
            self.response.content.decode(),
        )

    def test_assignment_requires_deviceassignment_view_permission(self):
        self.response = self.client.get(reverse("dashboard:index"))
        self.assertNotIn(
            assignments_link,
            self.response.content.decode(),
        )
        self.user.user_permissions.add(
            get_permission(DeviceAssignment, "view_deviceassignment")
        )
        self.response = self.client.get(reverse("dashboard:index"))
        self.assertIn(
            assignments_link,
            self.response.content.decode(),
        )

    def test_default_links_exist(self):
        self.response = self.client.get(reverse("dashboard:index"))
        for link in DEFAULT_LINKS:
            self.assertInHTML(
                link,
                self.response.content.decode(),
            )
