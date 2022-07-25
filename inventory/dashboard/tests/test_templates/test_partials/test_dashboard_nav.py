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

devices_link_selector = 'a[href="/devices/"]'
people_link_selector = 'a[href="/people/"]'
assignments_link_selector = 'a[href="/assignments/"]'

default_context = Context(
    {
        "perms": {
            "assignments": {
                "view_deviceassignment": True,
            },
            "devices": {
                "view_device": True,
            },
            "people": {
                "view_person": True,
            },
        },
    }
)

default_template = Template("{% include  'dashboard/partials/dashboard_nav.html'%}")


class DashboardNavTest(SimpleTestCase):
    def test_all_links_exist(self):
        context = copy.deepcopy(default_context)
        template = copy.deepcopy(default_template)
        rendered = template.render(context)
        soup = BeautifulSoup(rendered, "html.parser")

        devices_link = soup.select(devices_link_selector)
        people_link = soup.select(people_link_selector)
        assignments_link = soup.select(assignments_link_selector)

        self.assertEqual(len(devices_link), 1)
        self.assertEqual(len(people_link), 1)
        self.assertEqual(len(assignments_link), 1)

        self.assertInHTML(devices_link[0].contents[0], "Devices")
        self.assertInHTML(people_link[0].contents[0], "People")
        self.assertInHTML(assignments_link[0].contents[0], "Assignments")


class DashboardNavWithoutPermissionTest(SimpleTestCase):
    def setUp(self):
        self.context = copy.deepcopy(default_context)
        self.template = copy.deepcopy(default_template)

    def test_devices_link_missing(self):
        self.context["perms"]["devices"]["view_device"] = False
        rendered = self.template.render(self.context)
        soup = BeautifulSoup(rendered, "html.parser")
        devices_link = soup.select(devices_link_selector)
        people_link = soup.select(people_link_selector)
        assignments_link = soup.select(assignments_link_selector)
        self.assertEqual(len(devices_link), 0)
        self.assertEqual(len(people_link), 1)
        self.assertEqual(len(assignments_link), 1)

    def test_people_link_missing(self):
        self.context["perms"]["people"]["view_person"] = False
        rendered = self.template.render(self.context)
        soup = BeautifulSoup(rendered, "html.parser")
        devices_link = soup.select(devices_link_selector)
        people_link = soup.select(people_link_selector)
        assignments_link = soup.select(assignments_link_selector)
        self.assertEqual(len(devices_link), 1)
        self.assertEqual(len(people_link), 0)
        self.assertEqual(len(assignments_link), 1)

    def test_assignments_link_missing(self):
        self.context["perms"]["assignments"]["view_deviceassignment"] = False
        rendered = self.template.render(self.context)
        soup = BeautifulSoup(rendered, "html.parser")
        devices_link = soup.select(devices_link_selector)
        people_link = soup.select(people_link_selector)
        assignments_link = soup.select(assignments_link_selector)
        self.assertEqual(len(devices_link), 1)
        self.assertEqual(len(people_link), 1)
        self.assertEqual(len(assignments_link), 0)
