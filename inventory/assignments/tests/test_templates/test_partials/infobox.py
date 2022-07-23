from django.test import SimpleTestCase
from django.template import Context, Template
from bs4 import BeautifulSoup
import copy

list_link_selector = 'a[href="/assignments/"]'
update_link_selector = 'a[href="/assignments/1/edit/"]'
delete_link_selector = 'a[href="/assignments/1/delete/"]'

default_context = Context(
    {
        "deviceassignment": {
            "id": 1,
            "person": "Test Person",
            "device": "Test Device",
            "assignment_datetime": "21/7/2022 8:57 PM",
            "return_datetime": "",
        }
    }
)

default_template = Template(
    "{% include  'assignments/partials/deviceassignment_infobox.html'%}"
)


class DeviceAssignmentInfoboxTest(SimpleTestCase):
    def setUp(self):
        self.context = copy.deepcopy(default_context)
        self.template = copy.deepcopy(default_template)

    def test_fields_exist(self):
        expected_fields = [
            {
                "label": "Assignment ID :",
                "value": self.context["deviceassignment"]["id"],
            },
            {
                "label": "Person :",
                "value": self.context["deviceassignment"]["person"],
            },
            {
                "label": "Device :",
                "value": self.context["deviceassignment"]["device"],
            },
            {
                "label": "Assignment Date :",
                "value": "07/21/2022 8:57 p.m.",
            },
            {
                "label": "Return Date :",
                "value": self.context["deviceassignment"]["return_datetime"],
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

    def test_bottom_infbox_card(self):
        pass


class DeviceAssignmentInfoboxTestold(SimpleTestCase):
    def test_view_link_missing(self):
        self.context["perms"]["assignments"]["view_deviceassignment"] = False
        rendered = self.template.render(self.context)
        soup = BeautifulSoup(rendered, "html.parser")
        list_link = soup.select(list_link_selector)
        update_link = soup.select(update_link_selector)
        delete_link = soup.select(delete_link_selector)
        self.assertEqual(len(list_link), 0)
        self.assertEqual(len(update_link), 1)
        self.assertEqual(len(delete_link), 1)

    def test_update_link_missing(self):
        self.context["perms"]["assignments"]["change_deviceassignment"] = False
        rendered = self.template.render(self.context)
        soup = BeautifulSoup(rendered, "html.parser")
        list_link = soup.select(list_link_selector)
        update_link = soup.select(update_link_selector)
        delete_link = soup.select(delete_link_selector)
        print(self.context)
        self.assertEqual(len(list_link), 1)
        self.assertEqual(len(update_link), 0)
        self.assertEqual(len(delete_link), 1)

    def test_delete_link_missing(self):
        self.context["perms"]["assignments"]["delete_deviceassignment"] = False
        rendered = self.template.render(self.context)
        soup = BeautifulSoup(rendered, "html.parser")
        list_link = soup.select(list_link_selector)
        update_link = soup.select(update_link_selector)
        delete_link = soup.select(delete_link_selector)
        self.assertEqual(len(list_link), 1)
        self.assertEqual(len(update_link), 1)
        self.assertEqual(len(delete_link), 0)
