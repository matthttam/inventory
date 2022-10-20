from assignments.models import DeviceAssignment
from assignments.tests.factories import DeviceAssignmentFactory
from authentication.tests.factories import SuperuserUserFactory, User, UserFactory
from bs4 import BeautifulSoup
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase
from django.urls import reverse
from inventory.tests.helpers import (
    get_chrome_driver,
    get_permission,
    RealTransactionalStaticLiveServerTestCase,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from seleniumlogin import force_login


class DeviceAssignmentListWithViewPermissionLiveTest(StaticLiveServerTestCase):
    """
    Checks that the Detail List loads the appropriate links
    when the user only has permission to view devices
    """

    fixtures = ["contenttypes", "auth_permission", "auth_view_user"]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = get_chrome_driver()
        # UserFactory(
        #    username="view_user@example.com",
        #    user_permissions=[
        #        (DeviceAssignment, "view_deviceassignment"),
        #    ],
        # )
        cls.user = User.objects.get(username="view_user@example.com")
        force_login(cls.user, cls.browser, f"{cls.live_server_url}/")
        # DeviceAssignmentFactory()
        cls.browser.get(f"{cls.live_server_url}/assignments/")
        # WebDriverWait(cls.browser, 60).until(
        #    EC.presence_of_element_located((By.CLASS_NAME, "btn-toolbar"))
        # )
        # cls.soup = BeautifulSoup(cls.browser.page_source, "html.parser")
        print(cls.browser.page_source)

    @classmethod
    def tearDownClass(cls):
        # cls.browser.quit()
        super().tearDownClass()

    # def _fixture_setup(self):
    # pass

    def test_view_link_exists(self):
        view_link = self.soup.select_one('a[href="/assignments/1/"]')
        self.assertIsNotNone(view_link)

    def test_edit_link_missing(self):
        edit_link = self.soup.select_one('a[href="/assignments/1/edit/"]')
        self.assertIsNone(edit_link)

    def test_turnin_link_missing(self):
        turnin_link = self.soup.select_one('a[href="/assignments/1/turnin/"]')
        self.assertIsNone(turnin_link)

    def test_delete_link_missing(self):
        delete_link = self.soup.select_one('a[href="/assignments/1/delete/"]')
        self.assertIsNone(delete_link)


class DeviceAssignmentListWithTurninPermissionLiveTest(StaticLiveServerTestCase):
    """
    Checks that the Detail List loads the appropriate links
    when the user only has permission to view devices
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = get_chrome_driver()
        UserFactory(
            username="turnin_user@example.com",
            user_permissions=[
                (DeviceAssignment, "view_deviceassignment"),
                (DeviceAssignment, "turnin_deviceassignment"),
            ],
        )
        cls.user = User.objects.get(username="turnin_user@example.com")
        force_login(cls.user, cls.browser, f"{cls.live_server_url}/")
        DeviceAssignmentFactory()
        cls.browser.get(f"{cls.live_server_url}/assignments/")
        WebDriverWait(cls.browser, 60).until(
            EC.presence_of_element_located((By.CLASS_NAME, "btn-toolbar"))
        )
        cls.soup = BeautifulSoup(cls.browser.page_source, "html.parser")

    @classmethod
    def tearDownClass(cls):
        # cls.browser.quit()
        super().tearDownClass()

    def test_view_link_exists(self):
        view_link = self.soup.select_one('a[href="/assignments/1/"]')
        self.assertIsNotNone(view_link)

    def test_edit_link_missing(self):
        edit_link = self.soup.select_one('a[href="/assignments/1/edit/"]')
        self.assertIsNone(edit_link)

    def test_turnin_link_exists(self):
        turnin_link = self.soup.select_one('a[href="/assignments/1/turnin/"]')
        self.assertIsNotNone(turnin_link)

    def test_delete_link_missing(self):
        delete_link = self.soup.select_one('a[href="/assignments/1/delete/"]')
        self.assertIsNone(delete_link)
