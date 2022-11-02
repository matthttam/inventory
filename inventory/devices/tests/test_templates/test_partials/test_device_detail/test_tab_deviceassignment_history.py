from django.template.loader import render_to_string
from django.test import SimpleTestCase


class TabDeviceAssignmentHistoryTest(SimpleTestCase):
    """Tests the nav profile partial template"""

    def test_template_used(self):
        test_template = (
            "devices/partials/device_detail/tab_deviceassignment_history.html"
        )
        templates = [
            "devices/partials/device_detail/card_deviceassignment_history.html",
        ]

        for template in templates:
            with self.assertTemplateUsed(template):
                render_to_string(test_template)
