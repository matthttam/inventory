from django.test import SimpleTestCase
from django.urls import reverse

from authentication.tests.factories import SuperuserUserFactory, User, UserFactory

from devices.tests.factories import DeviceFactory
from django.template.loader import render_to_string


class DeviceDetailSuperuserTest(SimpleTestCase):
    """Checks that the Detail View loads the appropriate links"""

    def test_template_used(self):
        test_template = "devices/device_detail.html"
        templates = [
            "devices/partials/device_detail/inner_nav.html",
            "devices/partials/device_detail/sticky_header.html",
            "devices/partials/device_detail/tab_device_detail.html",
            "devices/partials/device_detail/tab_device_history.html",
            "devices/partials/device_detail/tab_deviceassignment_history.html",
        ]

        for template in templates:
            with self.assertTemplateUsed(template):
                render_to_string(test_template)

    def test_title(self):
        self.assertInHTML("Inventory - Device Detail", self.response.content.decode())
