import copy

from authentication.tests.factories import SuperuserUserFactory
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.template import Context, Template
from django.test import TestCase
from django.urls import reverse
from inventory.tests.helpers import get_chrome_driver, chrome_click_element
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from seleniumlogin import force_login


class DashboardTestSuperuser(TestCase):
    @classmethod
    def setUpTestData(cls):
        SuperuserUserFactory(username="my_superuser@example.com")

    def setUp(self):
        self.user = User.objects.get(username="my_superuser@example.com")
        self.client.force_login(self.user)
        self.response = self.client.get(reverse("dashboard:dashboard"))

    def test_templates(self):
        self.assertTemplateUsed(self.response, "base.html")
        self.assertTemplateUsed(self.response, "dashboard/partials/_side_nav.html")
        self.assertTemplateUsed(self.response, "dashboard/partials/_top_nav.html")


class DashboardTemplateTest(TestCase):
    def setUp(self):

        self.template = Template("{% include  'dashboard/dashboard.html'%}")
        self.context = Context(
            {
                "perms": {
                    "assignments": {
                        "view_deviceassignment": True,
                        "delete_deviceassignment": True,
                        "change_deviceassignment": True,
                    }
                },
            }
        )

    def test_quickassign_button_without_permission(self):
        context = copy.deepcopy(self.context)
        template = copy.deepcopy(self.template)
        context["perms"]["assignments"]["add_deviceassignment"] = False
        rendered = template.render(context)
        soup = BeautifulSoup(rendered, "html.parser")
        quickassign_link = soup.select('a[href="/assignments/quickassign/"]')
        self.assertEqual(
            len(quickassign_link),
            0,
            msg="Quick assign button exists when it should not!",
        )

    def test_quickassign_button_with_permissions(self):
        context = copy.deepcopy(self.context)
        template = copy.deepcopy(self.template)
        context["perms"]["assignments"]["add_deviceassignment"] = True
        rendered = template.render(context)
        soup = BeautifulSoup(rendered, "html.parser")
        quickassign_link = soup.select('a[href="/assignments/quickassign/"]')
        self.assertEqual(
            len(quickassign_link),
            1,
            msg="Quick assign button does not exist when it should!",
        )


class DashboardLiveTest(StaticLiveServerTestCase):
    def get_element(self, locator):
        return WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located(locator)
        )

        # (
        #            By.XPATH,
        #            '//*[@id="check_form"]/div[2]/div/span/span/span[1]/input',
        #        )

    def setUp(self):
        self.browser = get_chrome_driver()
        superuser = SuperuserUserFactory()
        force_login(superuser, self.browser, f"{self.live_server_url}/")
        self.browser.get(f"{self.live_server_url}/")

    def test_dashboard_becomes_active(self):
        # On page load dashboard should be active.
        dashboard_link = self.get_element((By.ID, "DashboardLink"))
        self.assertIn("active", dashboard_link.get_attribute("class"))

    def test_people_list_becomes_active(self):
        # Get People link
        people_link = self.get_element(
            (By.XPATH, '//a[@data-bs-target="#PeopleCollapse"]')
        )
        # Verify People is collapsed
        self.assertIn("collapsed", people_link.get_attribute("class"))

        # Click People
        chrome_click_element(self.browser, people_link)

        # Verify People is not collapsed
        self.assertNotIn("collapsed", people_link.get_attribute("class"))

        # Get People List link
        people_list_link = self.get_element(
            (By.XPATH, '//div[@id="PeopleCollapse"]/nav/a[@href="/people/"]')
        )
        # Verify People List link is not active
        self.assertNotIn("active", people_list_link.get_attribute("class"))

        # Click List
        chrome_click_element(self.browser, people_list_link)

        # Verify People Link is expanded and List is active
        people_link = self.get_element(
            (By.XPATH, '//a[@data-bs-target="#PeopleCollapse"]')
        )
        people_list_link = self.get_element(
            (By.XPATH, '//div[@id="PeopleCollapse"]/nav/a[@href="/people/"]')
        )
        self.assertNotIn("collapsed", people_link.get_attribute("class"))
        self.assertIn("active", people_list_link.get_attribute("class"))
