from datetime import datetime
from django.test import SimpleTestCase
from django.template import Context, Template
from bs4 import BeautifulSoup
from people.tests.factories import PersonFactory


class TableRowButtonsPermissionTest(SimpleTestCase):
    def setUp(self):
        person = PersonFactory.stub(id=1)
        self.context = Context(
            {
                "person": person,
                "perms": {
                    "people": {
                        "view_person": True,
                        "change_person": False,
                        "delete_person": False,
                    }
                },
            }
        )
        self.template = Template(
            "{% include  'people/partials/person_list/table_row_buttons.html'%}"
        )
        self.view_link_selector = 'a[href="/people/1/"]'
        self.edit_link_selector = 'a[href="/people/1/edit/"]'
        self.delete_link_selector = 'a[href="/people/1/delete/"]'

    def test_view_permissions(self):
        rendered = self.template.render(self.context)
        self.soup = BeautifulSoup(rendered, "html.parser")
        view_link = self.soup.select_one(self.view_link_selector)
        edit_link = self.soup.select_one(self.edit_link_selector)
        delete_link = self.soup.select_one(self.delete_link_selector)
        self.assertIsNotNone(view_link)
        self.assertIsNone(edit_link)
        self.assertIsNone(delete_link)

    def test_edit_permissions(self):
        self.context["perms"]["people"]["change_person"] = True
        rendered = self.template.render(self.context)
        self.soup = BeautifulSoup(rendered, "html.parser")
        view_link = self.soup.select_one(self.view_link_selector)
        edit_link = self.soup.select_one(self.edit_link_selector)
        delete_link = self.soup.select_one(self.delete_link_selector)
        self.assertIsNotNone(view_link)
        self.assertIsNotNone(edit_link)
        self.assertIsNone(delete_link)

    def test_delete_permissions(self):
        self.context["perms"]["people"]["delete_person"] = True
        rendered = self.template.render(self.context)
        self.soup = BeautifulSoup(rendered, "html.parser")
        view_link = self.soup.select_one(self.view_link_selector)
        edit_link = self.soup.select_one(self.edit_link_selector)
        delete_link = self.soup.select_one(self.delete_link_selector)
        self.assertIsNotNone(view_link)
        self.assertIsNone(edit_link)
        self.assertIsNotNone(delete_link)
