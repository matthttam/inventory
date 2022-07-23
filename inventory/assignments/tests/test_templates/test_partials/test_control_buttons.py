from django.test import TestCase, SimpleTestCase
from django.urls import reverse
from authentication.tests.factories import SuperuserUserFactory, User, UserFactory
from assignments.models import DeviceAssignment
from assignments.tests.factories import DeviceAssignmentFactory
from inventory.tests.helpers import get_permission

from django.template import Context, Template
from bs4 import BeautifulSoup
import copy

list_link = '<a class="btn btn-primary m-2" role="button" href="/assignments/">Assignment List</a>'
update_link = '<a class="btn btn-primary m-2" role="button" href="/assignments/1/edit/">Edit Assignment</a>'
delete_link = '<a class="btn btn-danger m-2" role="button" href="/assignments/1/delete/">Delete Assignment</a>'
list_link_selector = 'a[href="/assignments/"]'
update_link_selector = 'a[href="/assignments/1/edit/"]'
delete_link_selector = 'a[href="/assignments/1/delete/"]'

default_context = Context(
    {
        "deviceassignment": {"id": 1},
        "perms": {
            "assignments": {
                "view_deviceassignment": True,
                "delete_deviceassignment": True,
                "change_deviceassignment": True,
            }
        },
    }
)

default_template = Template(
    "{% include  'assignments/partials/deviceassignment_control_buttons.html'%}"
)


class DeviceAssignmentControlButtonsSuperuserTest(SimpleTestCase):
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

        self.assertEqual(list_link[0].contents[0], "Assignment List")
        self.assertEqual(update_link[0].contents[0], "Edit Assignment")
        self.assertEqual(delete_link[0].contents[0], "Delete Assignment")


class DeviceAssignmentControlButtonsWithoutPermissionTest(TestCase):
    def setUp(self):
        self.context = copy.deepcopy(default_context)
        self.template = copy.deepcopy(default_template)

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
