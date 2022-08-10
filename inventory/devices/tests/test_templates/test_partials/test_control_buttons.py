from django.test import SimpleTestCase
from django.template import Context, Template
from bs4 import BeautifulSoup
import copy

list_link_selector = 'a[href="/devices/"]'
update_link_selector = 'a[href="/devices/1/edit/"]'
delete_link_selector = 'a[href="/devices/1/delete/"]'

default_context = Context(
    {
        "device": {"id": 1},
        "perms": {
            "devices": {
                "view_device": True,
                "delete_device": True,
                "change_device": True,
            }
        },
    }
)

default_template = Template(
    "{% include  'devices/partials/device_control_buttons.html'%}"
)


class DeviceAssignmentControlButtonsTest(SimpleTestCase):
    def test_all_links_exist(self):
        context = copy.deepcopy(default_context)
        template = copy.deepcopy(default_template)
        rendered = template.render(context)
        soup = BeautifulSoup(rendered, "html.parser")

        list_link = soup.select(list_link_selector)
        update_link = soup.select(update_link_selector)
        delete_link = soup.select(delete_link_selector)

        self.assertEqual(len(list_link), 1)
        self.assertEqual(len(update_link), 1)
        self.assertEqual(len(delete_link), 1)

        self.assertInHTML(list_link[0].contents[0], "List")
        self.assertInHTML(update_link[0].contents[0], "Edit")
        self.assertInHTML(delete_link[0].contents[0], "Delete")


class DeviceAssignmentControlButtonsWithoutPermissionTest(SimpleTestCase):
    def setUp(self):
        self.context = copy.deepcopy(default_context)
        self.template = copy.deepcopy(default_template)

    def test_view_link_missing(self):
        self.context["perms"]["devices"]["view_device"] = False
        rendered = self.template.render(self.context)
        soup = BeautifulSoup(rendered, "html.parser")
        list_link = soup.select(list_link_selector)
        update_link = soup.select(update_link_selector)
        delete_link = soup.select(delete_link_selector)
        self.assertEqual(len(list_link), 0)
        self.assertEqual(len(update_link), 1)
        self.assertEqual(len(delete_link), 1)

    def test_update_link_missing(self):
        self.context["perms"]["devices"]["change_device"] = False
        rendered = self.template.render(self.context)
        soup = BeautifulSoup(rendered, "html.parser")
        list_link = soup.select(list_link_selector)
        update_link = soup.select(update_link_selector)
        delete_link = soup.select(delete_link_selector)
        self.assertEqual(len(list_link), 1)
        self.assertEqual(len(update_link), 0)
        self.assertEqual(len(delete_link), 1)

    def test_delete_link_missing(self):
        self.context["perms"]["devices"]["delete_device"] = False
        rendered = self.template.render(self.context)
        soup = BeautifulSoup(rendered, "html.parser")
        list_link = soup.select(list_link_selector)
        update_link = soup.select(update_link_selector)
        delete_link = soup.select(delete_link_selector)
        self.assertEqual(len(list_link), 1)
        self.assertEqual(len(update_link), 1)
        self.assertEqual(len(delete_link), 0)
