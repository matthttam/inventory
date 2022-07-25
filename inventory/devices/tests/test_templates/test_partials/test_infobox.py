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
            "person": "Test Person",
            "device": "Test Device",
            "assignment_datetime": datetime(2022, 7, 1, 2, 0, 0, 0),
            "return_datetime": "",
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
                "label": "Assignment ID :",
                "value": self.context["device"]["id"],
            },
            {
                "label": "Person :",
                "value": self.context["device"]["person"],
            },
            {
                "label": "Device :",
                "value": self.context["device"]["device"],
            },
            {
                "label": "Assignment Date :",
                "value": "07/01/2022 2 a.m.",
            },
            {
                "label": "Return Date :",
                "value": "",
            },
        ]
        context = copy.deepcopy(default_context)
        template = copy.deepcopy(default_template)
        rendered = template.render(context)
        soup = BeautifulSoup(rendered, "html.parser")

        info_divs = soup.select_one('p[name="assignment_card_body"]').find_all_next(
            "div", class_="row"
        )

        self.assertEqual(len(info_divs), len(expected_fields))
        for index, info_div in enumerate(info_divs):
            self.assertIn(str(expected_fields[index]["label"]), str(info_div))
            self.assertIn(str(expected_fields[index]["value"]), str(info_div))

    def test_bottom_infobox_card(self):
        """Verify providing a template for bottom_infobox_card loads that template"""
        context = copy.deepcopy(default_context)
        template = Template(
            "{% include 'devices/partials/device_infobox.html' with bottom_infobox_card='devices/partials/device_control_buttons.html' %}"
        )
        rendered = template.render(context)
        bottom_infobox_card_template = Template(
            "{% include 'devices/partials/device_control_buttons.html' %}"
        )
        bottom_infobox_card_rendered = bottom_infobox_card_template.render(context)
        self.assertIn(bottom_infobox_card_rendered, rendered)
