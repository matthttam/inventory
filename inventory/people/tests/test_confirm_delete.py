from django.test import TestCase
from django.urls import reverse

from authentication.tests.factories import SuperuserUserFactory, User, UserFactory

from bs4 import BeautifulSoup

from people.tests.factories import PersonFactory


class PersonConfirmDeleteTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        SuperuserUserFactory(username="my_superuser@example.com")

    def setUp(self):
        self.person = PersonFactory(
            id=1, first_name="Billy", last_name="Tucker", internal_id="1234"
        )
        self.user = User.objects.get(username="my_superuser@example.com")
        self.client.force_login(self.user)
        self.response = self.client.get(reverse("people:delete", args=[1]))

    def test_templates(self):
        self.assertTemplateUsed(self.response, "dashboard/dashboard.html")
        self.assertTemplateUsed(self.response, "people/partials/person_infobox.html")

    def test_title(self):
        self.assertInHTML(
            "Inventory - Person Confirm Delete", self.response.content.decode()
        )

    def test_buttons(self):
        soup = BeautifulSoup(self.response.content.decode(), "html.parser")
        submit_buttons = soup.select('button[type="submit"]')
        cancel_buttons = soup.select('a[href="/people/1/"]')
        self.assertEqual(len(submit_buttons), 1)
        self.assertEqual(len(cancel_buttons), 1)
        self.assertInHTML(submit_buttons[0].contents[0], f"Delete {self.person}")
        self.assertInHTML(cancel_buttons[0].contents[0], "Cancel")
