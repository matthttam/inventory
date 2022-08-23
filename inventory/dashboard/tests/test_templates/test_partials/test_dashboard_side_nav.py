from django.test import TestCase, SimpleTestCase
from django.urls import reverse
from authentication.tests.factories import UserFactory, SuperuserUserFactory
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from devices.models import Device
from people.models import Person
from assignments.models import DeviceAssignment
from inventory.tests.helpers import get_permission

from django.template import Context, Template
from django.test import SimpleTestCase
from bs4 import BeautifulSoup
import copy

device_list_selector = 'a[href="/devices/"]'
device_new_selector = 'a[href="/devices/new"]'

person_list_selector = 'a[href="/people/"]'
person_new_selector = 'a[href="/people/new"]'

assignment_list_selector = 'a[href="/assignments/"]'
assignment_new_selector = 'a[href="/assignments/new"]'
assignment_quickassign_selector = 'a[href="/assignments/quickassign"]'

admin_link_selector = 'a[href="/admin/"]'

default_context = Context(
    {
        "perms": {
            "assignments": {
                "view_deviceassignment": True,
                "add_deviceassignment": True,
            },
            "devices": {
                "view_device": True,
                "add_device": True,
            },
            "people": {
                "view_person": True,
                "add_person": True,
            },
        },
        "request": {
            "user": {
                "is_staff": True,
            }
        },
    }
)

default_template = Template("{% include  'dashboard/partials/_side_nav.html'%}")


class DashboardSideNavLinksTest(SimpleTestCase):
    def setUp(self):
        self.context = copy.deepcopy(default_context)
        self.template = copy.deepcopy(default_template)
        self.rendered = self.template.render(self.context)
        self.soup = BeautifulSoup(self.rendered, "html.parser")

    def test_dashboard_link(self):
        dashboard_link = self.soup.select_one("div.sb-sidenav-menu").select_one(
            'a[href="/"]'
        )
        self.assertInHTML("Dashboard", dashboard_link.text)
        print(dashboard_link)

    def test_all_links_exist(self):
        context = copy.deepcopy(default_context)
        template = copy.deepcopy(default_template)
        rendered = template.render(context)
        soup = BeautifulSoup(rendered, "html.parser")

        device_list = soup.select_one(device_list_selector)
        person_list = soup.select_one(person_list_selector)
        assignment_list = soup.select_one(assignment_list_selector)

        devices_new = soup.select_one(device_new_selector)
        people_new = soup.select_one(person_new_selector)
        assignments_new = soup.select_one(assignment_new_selector)

        admin_link = soup.select_one(admin_link_selector)

        self.assertEqual(len(device_list), 1)
        self.assertEqual(len(person_list), 1)
        self.assertEqual(len(assignment_list), 1)
        self.assertEqual(len(admin_link), 1)

        self.assertEqual(len(devices_new), 1)
        self.assertEqual(len(people_new), 1)
        self.assertEqual(len(assignments_new), 1)
        self.assertEqual(len(admin_link), 1)

        self.assertInHTML(device_list.text, "Devices")
        self.assertInHTML(person_list[0].text, "People")
        self.assertInHTML(assignment_list.text, "Assignments")
        self.assertInHTML(admin_link.text, "Admin")


class DashboardSideNavLinksWithoutPermissionTest(SimpleTestCase):
    def setUp(self):
        self.context = copy.deepcopy(default_context)
        self.template = copy.deepcopy(default_template)

    def test_devices_link_missing(self):
        self.context["perms"]["devices"]["view_device"] = False
        rendered = self.template.render(self.context)
        soup = BeautifulSoup(rendered, "html.parser")
        devices_link = soup.select(device_list_selector)
        self.assertEqual(len(devices_link), 0)

    def test_people_link_missing(self):
        self.context["perms"]["people"]["view_person"] = False
        rendered = self.template.render(self.context)
        soup = BeautifulSoup(rendered, "html.parser")
        people_link = soup.select(person_list_selector)
        self.assertEqual(len(people_link), 0)

    def test_assignments_link_missing(self):
        self.context["perms"]["assignments"]["view_deviceassignment"] = False
        rendered = self.template.render(self.context)
        soup = BeautifulSoup(rendered, "html.parser")
        assignments_link = soup.select(assignment_list_selector)
        self.assertEqual(len(assignments_link), 0)

    def test_admin_link_missing(self):
        self.context["request"]["user"]["is_staff"] = False
        rendered = self.template.render(self.context)
        soup = BeautifulSoup(rendered, "html.parser")
        admin_link = soup.select(admin_link_selector)
        self.assertEqual(len(admin_link), 0)
