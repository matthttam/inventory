from django.test import SimpleTestCase, TestCase
from django.template import Context, Template
from bs4 import BeautifulSoup
import copy
from devices.tests.factories import DeviceFactory
from django.urls import reverse
from zoneinfo import ZoneInfo
from authentication.tests.factories import SuperuserUserFactory
from datetime import datetime

list_link_selector = 'a[href="/devices/"]'
update_link_selector = 'a[href="/devices/1/edit/"]'
delete_link_selector = 'a[href="/devices/1/delete/"]'

default_context = Context(
    {
        "TIME_ZONE": "America/Chicago",
        "device": {
            "id": 1,
            "serial_number": "Test Serial",
            "asset_id": "Test Asset ID",
            "status": "Test Status",
            "device_model": "Test Model",
            "building": "Test Building",
            "room": "Test Room",
        },
        "perms": {
            "devices": {
                "view_device": True,
                "delete_device": True,
                "change_device": True,
            }
        },
    }
)

default_template = Template("{% include  'devices/partials/device_infobox.html'%}")


class DeviceInfoboxTest(SimpleTestCase):
    def setUp(self):
        self.context = copy.deepcopy(default_context)
        self.template = copy.deepcopy(default_template)

    def test_fields_exist(self):
        """Verify the infobox loads the assignment data expected"""
        expected_fields = [
            {
                "label": "Device ID :",
                "value": self.context["device"]["id"],
            },
            {
                "label": "Serial :",
                "value": self.context["device"]["serial_number"],
            },
            {
                "label": "Asset :",
                "value": self.context["device"]["asset_id"],
            },
            {
                "label": "Status :",
                "value": self.context["device"]["status"],
            },
            {
                "label": "Model :",
                "value": self.context["device"]["device_model"],
            },
            {
                "label": "Building :",
                "value": self.context["device"]["building"],
            },
            {
                "label": "Room :",
                "value": self.context["device"]["room"],
            },
        ]
        context = copy.deepcopy(default_context)
        template = copy.deepcopy(default_template)
        rendered = template.render(context)
        soup = BeautifulSoup(rendered, "html.parser")

        info_divs = soup.select_one('p[name="device_card_body"]').find_all_next(
            "div", class_="row"
        )
        self.assertEqual(len(info_divs), len(expected_fields))
        for index, info_div in enumerate(info_divs):
            label = info_div.select("div")[0].contents[0]
            value = info_div.select("div")[1].contents[0]
            self.assertEqual(
                str(expected_fields[index]["label"]),
                str(label),
            )
            self.assertEqual(
                str(expected_fields[index]["value"]),
                str(value),
            )

    def test_infobox_footer(self):
        """Verify providing a template for infobox_footer loads that template"""
        context = copy.deepcopy(default_context)
        template = Template(
            "{% include 'devices/partials/device_infobox.html' with infobox_footer='devices/partials/device_control_buttons.html' %}"
        )
        rendered = template.render(context)
        infobox_footer_template = Template(
            "{% include 'devices/partials/device_control_buttons.html' %}"
        )
        infobox_footer_rendered = infobox_footer_template.render(context)
        self.assertIn(infobox_footer_rendered, rendered)
