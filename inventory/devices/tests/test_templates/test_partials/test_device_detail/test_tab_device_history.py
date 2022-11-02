from django.template.loader import render_to_string
from django.test import SimpleTestCase


class TabDeviceHistoryTestTest(SimpleTestCase):
    """Tests the nav profile partial template"""

    def test_template_used(self):
        with self.assertTemplateUsed(
            "devices/partials/device_detail/card_device_history.html"
        ):
            render_to_string("devices/partials/device_detail/tab_device_history.html")
