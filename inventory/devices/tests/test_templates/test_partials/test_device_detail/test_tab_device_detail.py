from django.template.loader import render_to_string
from django.test import SimpleTestCase


class TabDeviceDetailTestTest(SimpleTestCase):
    """Tests the nav profile partial template"""

    def test_template_used(self):
        test_template = "devices/partials/device_detail/tab_device_detail.html"
        templates = [
            "devices/partials/device_detail/card_device_detail.html",
            "devices/partials/device_detail/card_outstanding_assignments.html",
            "devices/partials/device_detail/card_google_device_detail.html",
        ]

        for template in templates:
            with self.assertTemplateUsed(template):
                render_to_string(test_template)
