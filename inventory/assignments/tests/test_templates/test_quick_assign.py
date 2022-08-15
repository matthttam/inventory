from assignments.tests.factories import DeviceAssignmentFactory
from authentication.tests.factories import SuperuserUserFactory, User
from bs4 import BeautifulSoup
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import LiveServerTestCase, TestCase
from django.urls import reverse
from inventory.tests.helpers import chrome_set_value, get_chrome_driver
from people.tests.factories import PersonFactory
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from seleniumlogin import force_login


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
        self.browser.get(f"{self.live_server_url}/assignments/quickassign/")

        self.device_search_xpath = (
            '//*[@id="check_form"]/div[1]/div/span/span/span[1]/input'
        )

        self.person_search_xpath = (
            '//*[@id="check_form"]/div[2]/div/span/span/span[1]/input'
        )

        self.device_search_box = self.browser.find_element(
            by=By.XPATH,
            value=self.device_search_xpath,
        )

        self.person_search_box = self.browser.find_element(
            by=By.XPATH,
            value=self.person_search_xpath,
        )

    def test_device_search_is_focused_load(self):

        # person_searchbox = locate_with
        self.assertEqual(
            self.device_search_box,
            self.browser.switch_to.active_element,
            msg="Device search box is not focused automatically!",
        )

    def test_device_search_uses_asset(self):
        pass

    def test_device_search_uses_serial(self):
        pass

    def test_person_search_uses_internal_id(self):
        pass

        PersonFactory.create_batch(lastname="smith")
        chrome_set_value(self.browser, self.person_search_box, "smi")

        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.NAME, "person_search"))
        )

        search_results = self.browser.find_element(
            by=By.XPATH,
            value='//*[@id="select2-person-results"]',
        )
        print(search_results)
        # print(dir(self.browser))
        # self.assertEqual(self.browser.switchTo())
