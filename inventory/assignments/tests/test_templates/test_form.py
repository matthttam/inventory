from django.test import TestCase
from django.urls import reverse
from authentication.tests.factories import SuperuserUserFactory, User, UserFactory
from assignments.models import DeviceAssignment
from assignments.tests.factories import DeviceAssignmentFactory
from inventory.tests.helpers import get_permission
from bs4 import BeautifulSoup


class DeviceAssignmentFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        SuperuserUserFactory(username="my_superuser@example.com")
        DeviceAssignmentFactory(id=1)

    def setUp(self):
        self.user = User.objects.get(username="my_superuser@example.com")
        self.client.force_login(self.user)
        self.response = self.client.get(reverse("assignments:edit", args=[1]))

    def test_templates(self):
        self.assertTemplateUsed(self.response, "dashboard/dashboard.html")

    def test_title(self):
        self.assertInHTML("Inventory - Assignment Edit", self.response.content.decode())

    def test_buttons(self):
        soup = BeautifulSoup(self.response.content.decode(), "html.parser")
        print(self.response.content.decode())
        submit_buttons = soup.find("form").select('a[type="submit"]')
        cancel_buttons = soup.find("form").select('a[href="/assignments/"]')
        self.assertEqual(len(submit_buttons), 1)
        self.assertEqual(len(cancel_buttons), 1)
        self.assertEqual(submit_buttons[0].contents[0], "Save")
        self.assertEqual(cancel_buttons[0].contents[0], "Cancel")
