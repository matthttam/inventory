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
        "user": {"profile": {"display_name": "test_name"}},
    }
)

default_template = Template("{% include  'dashboard/partials/_side_nav.html'%}")


class DashboardSideNavTest(SimpleTestCase):
    def setUp(self) -> None:
        self.context = copy.deepcopy(default_context)
        self.template = copy.deepcopy(default_template)
        self.rendered = self.template.render(self.context)
        self.soup = BeautifulSoup(self.rendered, "html.parser")

    def test_sidenav_footer(self):
        side_nav_footer = self.soup.select_one("div.sb-sidenav-footer")
        logged_in_as = side_nav_footer.select('div[name="logged_in_as"]')
        self.assertInHTML("Logged in as:", str(side_nav_footer))
        self.assertInHTML("test_name", str(logged_in_as))


class DashboardSideNavLinksTest(SimpleTestCase):
    def setUp(self):
        self.context = copy.deepcopy(default_context)
        self.template = copy.deepcopy(default_template)
        self.rendered = self.template.render(self.context)
        self.soup = BeautifulSoup(self.rendered, "html.parser")

    def test_dashboard_link(self):
        dashboard_link = self.soup.select_one('a[href="/"]')
        self.assertInHTML("Dashboard", dashboard_link.text)

    ### People Links ###
    def test_people_link(self):
        person_link = self.soup.find("a", {"data-bs-target": "#PeopleCollapse"})
        self.assertInHTML("People", person_link.text)

    def test_people_list_link(self):
        person_list_link = self.soup.select_one("div#PeopleCollapse").select_one(
            'a[href="/people/"]'
        )
        self.assertInHTML("List", person_list_link.text)

    def test_people_create_link(self):
        person_create_link = self.soup.select_one("div#PeopleCollapse").select_one(
            'a[href="/people/new/"]'
        )
        self.assertInHTML("Create", person_create_link.text)

    ### Devices Links ###
    def test_devices_link(self):
        device_link = self.soup.find("a", {"data-bs-target": "#DevicesCollapse"})
        self.assertInHTML("Devices", device_link.text)

    def test_devices_list_link(self):
        device_list_link = self.soup.select_one("div#DevicesCollapse").select_one(
            'a[href="/devices/"]'
        )
        self.assertInHTML("List", device_list_link.text)

    def test_devices_create_link(self):
        person_create_link = self.soup.select_one("div#DevicesCollapse").select_one(
            'a[href="/devices/new/"]'
        )
        self.assertInHTML("Create", person_create_link.text)

    ### Assignments Links ###
    def test_assignments_link(self):
        assignment_link = self.soup.find(
            "a", {"data-bs-target": "#AssignmentsCollapse"}
        )
        self.assertInHTML("Assignments", assignment_link.text)

    def test_assignments_list_link(self):
        assignment_list_link = self.soup.select_one(
            "div#AssignmentsCollapse"
        ).select_one('a[href="/assignments/"]')
        self.assertInHTML("List", assignment_list_link.text)

    def test_assignments_quickassign_link(self):
        assignment_create_link = self.soup.select_one(
            "div#AssignmentsCollapse"
        ).select_one('a[href="/assignments/quickassign/"]')
        self.assertInHTML("Quick Assign", assignment_create_link.text)

    def test_assignments_create_link(self):
        assignment_create_link = self.soup.select_one(
            "div#AssignmentsCollapse"
        ).select_one('a[href="/assignments/new/"]')
        self.assertInHTML("Create", assignment_create_link.text)

    ### Admin Links ###
    def test_administration_link(self):
        admin_link = self.soup.find("a", {"data-bs-target": "#AdminCollapse"})
        self.assertInHTML("Administration", admin_link.text)

    def test_administration_management_portal_link(self):
        administration_managemenet_portal_link = self.soup.select_one(
            "div#AdminCollapse"
        ).select_one('a[href="/admin/"]')
        self.assertInHTML(
            "Management Portal", administration_managemenet_portal_link.text
        )


class DashboardSideNavLinksWithoutPermissionTest(SimpleTestCase):
    def setUp(self):
        self.context = copy.deepcopy(default_context)
        self.template = copy.deepcopy(default_template)

    ### People Links ###
    def test_people_links_missing_missing_view_person_rights(self):
        self.context["perms"]["people"]["view_person"] = False
        rendered = self.template.render(self.context)
        soup = BeautifulSoup(rendered, "html.parser")

        person_link = soup.find("a", {"data-bs-target": "#PeopleCollapse"})
        self.assertIsNone(person_link)

        person_list_link = soup.select_one('a[href="/people/"]')
        self.assertIsNone(person_list_link)

        person_create_link = soup.select_one('a[href="/people/new/"]')
        self.assertIsNone(person_create_link)

    def test_people_links_missing_missing_add_person_rights(self):
        self.context["perms"]["people"]["add_person"] = False
        rendered = self.template.render(self.context)
        soup = BeautifulSoup(rendered, "html.parser")

        person_link = soup.find("a", {"data-bs-target": "#PeopleCollapse"})
        self.assertIsNotNone(person_link)

        person_list_link = soup.select_one('a[href="/people/"]')
        self.assertIsNotNone(person_list_link)

        person_create_link = soup.select_one('a[href="/people/new/"]')
        self.assertIsNone(person_create_link)

    ### Devices Links ###
    def test_devices_links_missing_missing_view_device_rights(self):
        self.context["perms"]["devices"]["view_device"] = False
        rendered = self.template.render(self.context)
        soup = BeautifulSoup(rendered, "html.parser")

        device_link = soup.find("a", {"data-bs-target": "#DevicesCollapse"})
        self.assertIsNone(device_link)

        device_list_link = soup.select_one('a[href="/devices/"]')
        self.assertIsNone(device_list_link)

        device_create_link = soup.select_one('a[href="/devices/new/"]')
        self.assertIsNone(device_create_link)

    def test_devices_links_missing_missing_add_device_rights(self):
        self.context["perms"]["devices"]["add_device"] = False
        rendered = self.template.render(self.context)
        soup = BeautifulSoup(rendered, "html.parser")

        device_link = soup.find("a", {"data-bs-target": "#DevicesCollapse"})
        self.assertIsNotNone(device_link)

        device_list_link = soup.select_one('a[href="/devices/"]')
        self.assertIsNotNone(device_list_link)

        device_create_link = soup.select_one('a[href="/devices/new/"]')
        self.assertIsNone(device_create_link)

    ### Assignments Links ###
    def test_assignments_links_missing_view_assignment_rights(self):
        self.context["perms"]["assignments"]["view_deviceassignment"] = False
        rendered = self.template.render(self.context)
        soup = BeautifulSoup(rendered, "html.parser")

        assignment_link = soup.find("a", {"data-bs-target": "#AssignmentsCollapse"})
        self.assertIsNone(assignment_link)

        assignment_list_link = soup.select_one('a[href="/assignments/"]')
        self.assertIsNone(assignment_list_link)

        assignment_create_link = soup.select_one('a[href="/assignments/new/"]')
        self.assertIsNone(assignment_create_link)

    def test_assignments_links_missing_add_assignment_rights(self):
        self.context["perms"]["assignments"]["add_deviceassignment"] = False
        rendered = self.template.render(self.context)
        soup = BeautifulSoup(rendered, "html.parser")

        assignment_link = soup.find("a", {"data-bs-target": "#AssignmentsCollapse"})
        self.assertIsNotNone(assignment_link)

        assignment_list_link = soup.select_one('a[href="/assignments/"]')
        self.assertIsNotNone(assignment_list_link)

        assignment_create_link = soup.select_one('a[href="/assignments/new/"]')
        self.assertIsNone(assignment_create_link)

    ### Admin ###
    def test_admin_links_when_not_staff(self):
        self.context["request"]["user"]["is_staff"] = False
        rendered = self.template.render(self.context)
        soup = BeautifulSoup(rendered, "html.parser")

        administration_link = soup.find("a", {"data-bs-target": "#AdminCollapse"})
        self.assertIsNone(administration_link)

        administration_management_portal_link = soup.select_one(
            'a[href="/assignments/"]'
        )
        self.assertIsNotNone(administration_management_portal_link)
