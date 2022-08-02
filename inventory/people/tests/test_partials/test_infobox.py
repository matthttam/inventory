from django.test import SimpleTestCase, TestCase
from django.template import Context, Template
from bs4 import BeautifulSoup
import copy
from people.tests.factories import PersonFactory
from django.urls import reverse
from zoneinfo import ZoneInfo
from authentication.tests.factories import SuperuserUserFactory
from datetime import datetime

list_link_selector = 'a[href="/people/"]'
update_link_selector = 'a[href="/people/1/edit/"]'
delete_link_selector = 'a[href="/people/1/delete/"]'

default_context = Context(
    {
        "TIME_ZONE": "America/Chicago",
        "person": {
            "id": 1,
            "first_name": "Test First Name",
            "last_name": "Test Last Name",
            "email": "Test Email",
            "primary_building" "Test Primary Building",
            "internal_id": "Test Internal ID",
            "type": "Test Type",
            "status": "Test Status",
        },
        "perms": {
            "people": {
                "view_person": True,
                "delete_person": True,
                "change_person": True,
            }
        },
    }
)

default_template = Template("{% include  'people/partials/person_infobox.html'%}")


class PersonInfoboxTest(SimpleTestCase):
    def setUp(self):
        self.context = copy.deepcopy(default_context)
        self.template = copy.deepcopy(default_template)

    def test_fields_exist(self):
        """Verify the infobox loads the person data expected"""
        expected_fields = [
            {
                "label": "Person ID :",
                "value": self.context["person"]["id"],
            },
            {
                "label": "First name :",
                "value": self.context["person"]["first_name"],
            },
            {
                "label": "Last name :",
                "value": self.context["person"]["last_name"],
            },
            {
                "label": "Email :",
                "value": self.context["person"]["email"],
            },
            {
                "label": "Primary Building :",
                "value": self.context["person"]["primary_building"],
            },
            {
                "label": "Internal ID :",
                "value": self.context["person"]["internal_id"],
            },
            {
                "label": "Type :",
                "value": self.context["person"]["type"],
            },
            {
                "label": "Status :",
                "value": self.context["person"]["status"],
            },
        ]
        context = copy.deepcopy(default_context)
        template = copy.deepcopy(default_template)
        rendered = template.render(context)
        soup = BeautifulSoup(rendered, "html.parser")

        info_divs = soup.select_one('p[name="person_card_body"]').find_all_next(
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

    def test_bottom_infobox_card(self):
        """Verify providing a template for bottom_infobox_card loads that template"""
        context = copy.deepcopy(default_context)
        template = Template(
            "{% include 'people/partials/person_infobox.html' with bottom_infobox_card='people/partials/person_control_buttons.html' %}"
        )
        rendered = template.render(context)
        bottom_infobox_card_template = Template(
            "{% include 'people/partials/person_control_buttons.html' %}"
        )
        bottom_infobox_card_rendered = bottom_infobox_card_template.render(context)
        self.assertIn(bottom_infobox_card_rendered, rendered)
