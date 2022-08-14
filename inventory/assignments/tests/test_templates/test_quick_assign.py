from assignments.tests.factories import DeviceAssignmentFactory
from authentication.tests.factories import SuperuserUserFactory, User
from bs4 import BeautifulSoup
from django.test import TestCase
from django.urls import reverse
from inventory.tests.helpers import chrome_set_value, get_chrome_driver
from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from seleniumlogin import force_login
from selenium.webdriver.common.by import By


class DeviceAssignmentQuickAssignTemplateTest(TestCase):
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


class DeviceAssignmentQuickAssignLiveTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = get_chrome_driver()
        superuser = SuperuserUserFactory()
        force_login(superuser, self.browser, f"{self.live_server_url}/")

    def test_quickassign_person_is_focused_load(self):
        self.browser.get(f"{self.live_server_url}/assignments/quickassign/")
        # person_searchbox = locate_with
        person_search_box = self.browser.find_element(
            by=By.XPATH,
            value='//*[@id="check_form"]/div[1]/div/span/span/span[1]/input',
        )
        self.assertEqual(
            person_search_box,
            self.browser.switch_to.active_element,
            msg="Device search box is not focused automatically!",
        )

        # print(dir(self.browser))
        # self.assertEqual(self.browser.switchTo())
