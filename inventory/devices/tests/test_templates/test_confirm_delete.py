from django.test import TestCase
from django.urls import reverse

from authentication.tests.factories import SuperuserUserFactory, User

from bs4 import BeautifulSoup

from devices.tests.factories import DeviceFactory


class DeviceConfirmDeleteTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        SuperuserUserFactory(username="my_superuser@example.com")

    def setUp(self):
        self.device = DeviceFactory(id=1)
        self.user = User.objects.get(username="my_superuser@example.com")
        self.client.force_login(self.user)
        self.response = self.client.get(reverse("devices:delete", args=[1]))

    def test_templates(self):
        self.assertTemplateUsed(self.response, "dashboard/dashboard.html")

    def test_title(self):
        self.assertInHTML(
            "Inventory - Device Confirm Delete", self.response.content.decode()
        )

    def test_buttons(self):
        soup = BeautifulSoup(self.response.content.decode(), "html.parser")
        submit_buttons = soup.select('button[type="submit"]')
        cancel_buttons = soup.select('a[href="/devices/1/"]')
        self.assertEqual(len(submit_buttons), 1)
        self.assertEqual(len(cancel_buttons), 1)
        self.assertInHTML(
            submit_buttons[0].contents[0],
            f"Delete {self.device}",
        )
        self.assertInHTML(cancel_buttons[0].contents[0], "Cancel")
