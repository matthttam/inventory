from django.test import TestCase
from django.urls import reverse
from authentication.tests.factories import SuperuserUserFactory, User, UserFactory
from devices.models import Device
from devices.tests.factories import DeviceFactory
from inventory.tests.helpers import get_permission
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

new_link = '<a class="btn btn-primary m-2" role="button" href="/devices/new/">Create Device</a>'

DEFAULT_LINKS = []
ALL_LINKS = [new_link]


class DeviceListSuperuserTest(TestCase):
    """Checks that the List View loads the appropriate links"""

    @classmethod
    def setUpTestData(cls):
        SuperuserUserFactory(username="my_superuser@example.com")
        DeviceFactory(id=1)

    def setUp(self):
        self.user = User.objects.get(username="my_superuser@example.com")
        self.client.force_login(self.user)
        self.response = self.client.get(reverse("devices:index"))

    def test_default_links_exist(self):
        if len(DEFAULT_LINKS) == 0:
            return
        for link in DEFAULT_LINKS:
            self.assertInHTML(
                link,
                self.response.content.decode(),
            )

    def test_all_links_exist(self):
        if len(ALL_LINKS) == 0:
            return
        for link in ALL_LINKS:
            self.assertInHTML(
                link,
                self.response.content.decode(),
            )

    def test_template_used(self):
        self.assertTemplateUsed(self.response, "devices/device_list.html")
        self.assertTemplateUsed(self.response, "dashboard/dashboard.html")
        self.assertTemplateUsed(self.response, "partials/datatables.html")

    def test_title(self):
        self.assertInHTML("Inventory - Devices", self.response.content.decode())


class DeviceListWithoutPermissionLiveTest(TestCase):
    """
    Checks that the Detail List loads the appropriate links
    when the user only has permission to view devices
    """

    @classmethod
    def setUpTestData(cls):
        UserFactory(username="my_regularuser@example.com")
        DeviceFactory(id=1)

    def setUp(self):
        self.user = User.objects.get(username="my_regularuser@example.com")
        self.client.force_login(self.user)
        self.response = self.client.get(reverse("devices:index"))

    def test_new_link(self):
        self.assertNotIn(
            new_link,
            self.response.content.decode(),
        )


class DeviceListWithPermissionTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        UserFactory(username="my_regularuser@example.com")
        DeviceFactory(id=1)

    def setUp(self):
        self.user = User.objects.get(username="my_regularuser@example.com")
        self.client.force_login(self.user)
        self.user.user_permissions.add(get_permission(Device, "view_device"))

    def test_new_link(self):
        self.user.user_permissions.add(get_permission(Device, "add_device"))
        self.response = self.client.get(reverse("devices:index"))
        self.assertInHTML(
            new_link,
            self.response.content.decode(),
        )
