from django.test import TestCase
from django.urls import reverse

from authentication.tests.factories import SuperuserUserFactory, User, UserFactory

from devices.tests.factories import DeviceFactory


class DeviceDetailSuperuserTest(TestCase):
    """Checks that the Detail View loads the appropriate links"""

    @classmethod
    def setUpTestData(cls):
        SuperuserUserFactory(username="my_superuser@example.com")
        DeviceFactory(id=1)

    def setUp(self):
        self.user = User.objects.get(username="my_superuser@example.com")
        self.client.force_login(self.user)
        self.response = self.client.get(reverse("devices:detail", args=[1]))

    def test_template_used(self):
        self.assertTemplateUsed(self.response, "devices/device_detail.html")
        self.assertTemplateUsed(self.response, "devices/partials/device_infobox.html")
        self.assertTemplateUsed(
            self.response, "devices/partials/device_control_buttons.html"
        )

    def test_title(self):
        self.assertInHTML("Inventory - Device Detail", self.response.content.decode())
