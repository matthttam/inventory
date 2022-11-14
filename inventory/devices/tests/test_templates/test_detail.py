from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from authentication.tests.factories import SuperuserUserFactory, User, UserFactory

from devices.tests.factories import DeviceFactory
from django.template.loader import render_to_string


class DeviceDetailTest(TestCase):
    """Checks that the Detail View loads with the appropriate templates and title"""

    @classmethod
    def setUpTestData(cls):
        SuperuserUserFactory(username="my_superuser@example.com")
        DeviceFactory(id=1)

    def setUp(self):
        self.user = User.objects.get(username="my_superuser@example.com")
        self.client.force_login(self.user)
        self.response = self.client.get(reverse("devices:detail", args=[1]))

    def test_template_used(self):
        templates = [
            "devices/partials/detail/inner_nav.html",
            "devices/partials/detail/sticky_header.html",
            "devices/partials/detail/tab_device_detail.html",
            "devices/partials/detail/tab_device_history.html",
            "devices/partials/detail/tab_deviceassignment_history.html",
        ]
        for template in templates:
            self.assertTemplateUsed(self.response, template)

    def test_title(self):
        self.assertInHTML("<title>Inventory - Device Detail</title>", self.response.content.decode())
