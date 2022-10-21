from datetime import datetime
from django.test import SimpleTestCase
from django.template import Context, Template
from bs4 import BeautifulSoup
from assignments.tests.factories import DeviceAssignmentFactory


class TableRowButtonsPermissionTest(SimpleTestCase):
    def setUp(self):
        deviceassignment = DeviceAssignmentFactory.build(id=1)
        self.context = Context(
            {
                "deviceassignment": deviceassignment,
                "perms": {
                    "assignments": {
                        "view_deviceassignment": True,
                        "change_deviceassignment": False,
                        "turnin_deviceassignment": False,
                        "delete_deviceassignment": False,
                    }
                },
            }
        )
        self.template = Template(
            "{% include  'assignments/partials/deviceassignment_list/table_row_buttons.html'%}"
        )
        self.view_link_selector = 'a[href="/assignments/1/"]'
        self.edit_link_selector = 'a[href="/assignments/1/edit/"]'
        self.turnin_link_selector = 'a[href="/assignments/1/turnin/"]'
        self.delete_link_selector = 'a[href="/assignments/1/delete/"]'

    def test_view_permissions(self):
        rendered = self.template.render(self.context)
        self.soup = BeautifulSoup(rendered, "html.parser")
        view_link = self.soup.select_one(self.view_link_selector)
        edit_link = self.soup.select_one(self.edit_link_selector)
        turnin_link = self.soup.select_one(self.turnin_link_selector)
        delete_link = self.soup.select_one(self.delete_link_selector)
        self.assertIsNotNone(view_link)
        self.assertIsNone(edit_link)
        self.assertIsNone(turnin_link)
        self.assertIsNone(delete_link)

    def test_edit_permissions(self):
        self.context["perms"]["assignments"]["change_deviceassignment"] = True
        rendered = self.template.render(self.context)
        self.soup = BeautifulSoup(rendered, "html.parser")
        view_link = self.soup.select_one(self.view_link_selector)
        edit_link = self.soup.select_one(self.edit_link_selector)
        turnin_link = self.soup.select_one(self.turnin_link_selector)
        delete_link = self.soup.select_one(self.delete_link_selector)
        self.assertIsNotNone(view_link)
        self.assertIsNotNone(edit_link)
        self.assertIsNone(turnin_link)
        self.assertIsNone(delete_link)

    def test_turnin_permissions(self):
        self.context["perms"]["assignments"]["turnin_deviceassignment"] = True
        rendered = self.template.render(self.context)
        self.soup = BeautifulSoup(rendered, "html.parser")
        view_link = self.soup.select_one(self.view_link_selector)
        edit_link = self.soup.select_one(self.edit_link_selector)
        turnin_link = self.soup.select_one(self.turnin_link_selector)
        delete_link = self.soup.select_one(self.delete_link_selector)
        self.assertIsNotNone(view_link)
        self.assertIsNone(edit_link)
        self.assertIsNotNone(turnin_link)
        self.assertIsNone(delete_link)
        self.assertFalse(
            "disabled" in turnin_link.attrs["class"],
            msg="Turnin button is disabled when assignment is not turned in yet!",
        )

    def test_delete_permissions(self):
        self.context["perms"]["assignments"]["delete_deviceassignment"] = True
        rendered = self.template.render(self.context)
        self.soup = BeautifulSoup(rendered, "html.parser")
        view_link = self.soup.select_one(self.view_link_selector)
        edit_link = self.soup.select_one(self.edit_link_selector)
        turnin_link = self.soup.select_one(self.turnin_link_selector)
        delete_link = self.soup.select_one(self.delete_link_selector)
        self.assertIsNotNone(view_link)
        self.assertIsNone(edit_link)
        self.assertIsNone(turnin_link)
        self.assertIsNotNone(delete_link)

    def test_turnin_disabled_when_turned_in(self):
        self.context["perms"]["assignments"]["turnin_deviceassignment"] = True
        self.context["deviceassignment"].return_datetime = datetime.now()
        rendered = self.template.render(self.context)
        self.soup = BeautifulSoup(rendered, "html.parser")
        turnin_link = self.soup.select_one(self.turnin_link_selector)
        self.assertIsNotNone(turnin_link)
        self.assertTrue(
            "disabled" in turnin_link.attrs["class"],
            msg="Turnin button is enabled when assignment is already turned in!",
        )
