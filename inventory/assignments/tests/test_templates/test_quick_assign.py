from django.test import TestCase
from django.urls import reverse

from bs4 import BeautifulSoup

from authentication.tests.factories import SuperuserUserFactory, User
from assignments.tests.factories import DeviceAssignmentFactory


class DeviceAssignmentQuickAssignFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        SuperuserUserFactory(username="my_superuser@example.com")
        DeviceAssignmentFactory(id=1)

    def setUp(self):
        self.user = User.objects.get(username="my_superuser@example.com")
        self.client.force_login(self.user)
        self.response = self.client.get(reverse("assignments:quickassign"))

    def test_templates(self):
        self.assertTemplateUsed(self.response, "dashboard/dashboard.html")

    def test_title(self):
        self.assertInHTML("Inventory - Quick Assign", self.response.content.decode())

    def test_buttons(self):
        soup = BeautifulSoup(self.response.content.decode(), "html.parser")
        submit_buttons = soup.find("form").select('button[type="submit"]')
        self.assertEqual(len(submit_buttons), 1)
        self.assertInHTML(submit_buttons[0].contents[0], "Submit")