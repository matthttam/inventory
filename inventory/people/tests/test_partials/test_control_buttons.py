from django.test import SimpleTestCase
from django.template import Context, Template
from bs4 import BeautifulSoup
import copy

list_link_selector = 'a[href="/people/"]'
update_link_selector = 'a[href="/people/1/edit/"]'
delete_link_selector = 'a[href="/people/1/delete/"]'

default_context = Context(
    {
        "person": {"id": 1},
        "perms": {
            "people": {
                "view_person": True,
                "delete_person": True,
                "change_person": True,
            }
        },
    }
)

default_template = Template(
    "{% include  'people/partials/person_control_buttons.html'%}"
)


class PersonControlButtonsTest(SimpleTestCase):
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


class PersonControlButtonsWithoutPermissionTest(SimpleTestCase):
    def setUp(self):
        self.context = copy.deepcopy(default_context)
        self.template = copy.deepcopy(default_template)

    def test_view_link_missing(self):
        self.context["perms"]["people"]["view_person"] = False
        rendered = self.template.render(self.context)
        soup = BeautifulSoup(rendered, "html.parser")
        list_link = soup.select(list_link_selector)
        update_link = soup.select(update_link_selector)
        delete_link = soup.select(delete_link_selector)
        self.assertEqual(len(list_link), 0)
        self.assertEqual(len(update_link), 1)
        self.assertEqual(len(delete_link), 1)

    def test_update_link_missing(self):
        self.context["perms"]["people"]["change_person"] = False
        rendered = self.template.render(self.context)
        soup = BeautifulSoup(rendered, "html.parser")
        list_link = soup.select(list_link_selector)
        update_link = soup.select(update_link_selector)
        delete_link = soup.select(delete_link_selector)
        self.assertEqual(len(list_link), 1)
        self.assertEqual(len(update_link), 0)
        self.assertEqual(len(delete_link), 1)

    def test_delete_link_missing(self):
        self.context["perms"]["people"]["delete_person"] = False
        rendered = self.template.render(self.context)
        soup = BeautifulSoup(rendered, "html.parser")
        list_link = soup.select(list_link_selector)
        update_link = soup.select(update_link_selector)
        delete_link = soup.select(delete_link_selector)
        self.assertEqual(len(list_link), 1)
        self.assertEqual(len(update_link), 1)
        self.assertEqual(len(delete_link), 0)
