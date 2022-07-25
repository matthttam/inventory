from django.test import TestCase
from django.urls import reverse

from authentication.tests.factories import SuperuserUserFactory, User

from bs4 import BeautifulSoup

from assignments.tests.factories import DeviceAssignmentFactory


class DeviceAssignmentConfirmDeleteTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        SuperuserUserFactory(username="my_superuser@example.com")
        DeviceAssignmentFactory(id=1)

    def setUp(self):
        self.user = User.objects.get(username="my_superuser@example.com")
        self.client.force_login(self.user)
        self.response = self.client.get(reverse("assignments:delete", args=[1]))

    def test_templates(self):
        self.assertTemplateUsed(self.response, "dashboard/dashboard.html")
        self.assertTemplateUsed(
            self.response, "assignments/partials/deviceassignment_infobox.html"
        )

    def test_title(self):
        self.assertInHTML(
            "Inventory - Assignment Confirm Delete", self.response.content.decode()
        )

    def test_buttons(self):
        soup = BeautifulSoup(self.response.content.decode(), "html.parser")
        submit_buttons = soup.select('button[type="submit"]')
        cancel_buttons = soup.select('a[href="/assignments/1/"]')
        self.assertEqual(len(submit_buttons), 1)
        self.assertEqual(len(cancel_buttons), 1)
        self.assertInHTML(submit_buttons[0].contents[0], "Delete Assignment 1")
        self.assertInHTML(cancel_buttons[0].contents[0], "Cancel")
