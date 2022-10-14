from django.test import TestCase
from django.urls import reverse
from authentication.tests.factories import SuperuserUserFactory, User, UserFactory
from assignments.models import DeviceAssignment
from assignments.tests.factories import DeviceAssignmentFactory
from inventory.tests.helpers import get_permission
from bs4 import BeautifulSoup
from inventory.tests.helpers import get_driver  # , get_firefox_driver,
from seleniumlogin import force_login
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from pyvirtualdisplay import Display
from inventory.tests.helpers import get_chrome_driver, chrome_click_element
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class DeviceAssignmentListSuperuserTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        SuperuserUserFactory(username="my_superuser@example.com")
        DeviceAssignmentFactory(id=1)

    def setUp(self):
        self.user = User.objects.get(username="my_superuser@example.com")
        self.client.force_login(self.user)
        self.user.user_permissions.add(
            get_permission(DeviceAssignment, "view_deviceassignment")
        )
        self.response = self.client.get(reverse("assignments:index"))
        self.soup = BeautifulSoup(self.response.content.decode(), "html.parser")

    def test_template_used(self):
        self.assertTemplateUsed(self.response, "assignments/deviceassignment_list.html")
        self.assertTemplateUsed(self.response, "dashboard/dashboard.html")
        self.assertTemplateUsed(self.response, "partials/datatables.html")

    def test_valid_html(self):
        self.assertInHTML("Inventory - Assignments", self.response.content.decode())

    def test_title(self):
        self.assertEqual("Inventory - Assignments", self.soup.title.string)


class DeviceAssignmentListSuperuserLiveTest(StaticLiveServerTestCase):
    """Checks that the List View loads the appropriate links"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = get_chrome_driver()
        SuperuserUserFactory(username="my_superuser@example.com")
        cls.user = User.objects.get(username="my_superuser@example.com")
        force_login(cls.user, cls.browser, f"{cls.live_server_url}/")
        DeviceAssignmentFactory(id=1)
        cls.browser.get(f"{cls.live_server_url}/assignments/")
        WebDriverWait(cls.browser, 60).until(
            EC.presence_of_element_located((By.CLASS_NAME, "btn-toolbar"))
        )
        cls.soup = BeautifulSoup(cls.browser.page_source, "html.parser")

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def setUp(self):
        pass

    def test_action_header(self):
        action_header = self.soup.find("th", string="Action")
        self.assertIsNotNone(action_header)

    def test_view_link(self):
        view_link = self.soup.select_one('a[href="/assignments/1/"]')
        self.assertIsNotNone(view_link)

    def test_edit_link(self):
        edit_link = self.soup.select_one('a[href="/assignments/1/edit/"]')
        self.assertIsNotNone(edit_link)

    def test_turnin_link(self):
        turnin_link = self.soup.select_one('a[href="/assignments/1/turnin/"]')
        self.assertIsNotNone(turnin_link)

    def test_delete_link(self):
        delete_link = self.soup.select_one('a[href="/assignments/1/delete/"]')
        self.assertIsNotNone(delete_link)


class DeviceAssignmentListWithoutPermissionLiveTest(StaticLiveServerTestCase):
    """
    Checks that the Detail List loads the appropriate links
    when the user only has permission to view devices
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = get_chrome_driver()
        user = UserFactory(username="my_regularuser@example.com")
        user.user_permissions.add(
            get_permission(DeviceAssignment, "view_deviceassignment")
        )
        user.save()
        cls.user = User.objects.get(username="my_regularuser@example.com")
        force_login(cls.user, cls.browser, f"{cls.live_server_url}/")
        DeviceAssignmentFactory(id=1)
        cls.browser.get(f"{cls.live_server_url}/assignments/")
        WebDriverWait(cls.browser, 60).until(
            EC.presence_of_element_located((By.CLASS_NAME, "btn-toolbar"))
        )
        cls.soup = BeautifulSoup(cls.browser.page_source, "html.parser")

    def setUp(self):
        pass

    def test_view_link(self):
        view_link = self.soup.select_one('a[href="/assignments/1/"]')
        self.assertIsNotNone(view_link)

    def test_edit_link(self):
        edit_link = self.soup.select_one('a[href="/assignments/1/edit/"]')
        self.assertIsNone(edit_link)

    def test_turnin_link(self):
        turnin_link = self.soup.select_one('a[href="/assignments/1/turnin/"]')
        self.assertIsNone(turnin_link)

    def test_delete_link(self):
        delete_link = self.soup.select_one('a[href="/assignments/1/delete/"]')
        self.assertIsNone(delete_link)


class DeviceAssignmentListWithPermissionLiveTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = get_chrome_driver()

        cls.user = User.objects.get(username="my_regularuser@example.com")
        force_login(cls.user, cls.browser, f"{cls.live_server_url}/")
        DeviceAssignmentFactory(id=1)

        user.user_permissions.add(
            get_permission(DeviceAssignment, "view_deviceassignment")
        )
        user.save()
        cls.user = User.objects.get(username="my_regularuser@example.com")
        force_login(cls.user, cls.browser, f"{cls.live_server_url}/")
        DeviceAssignmentFactory(id=1)
        cls.browser.get(f"{cls.live_server_url}/assignments/")
        WebDriverWait(cls.browser, 60).until(
            EC.presence_of_element_located((By.CLASS_NAME, "btn-toolbar"))
        )
        cls.soup = BeautifulSoup(cls.browser.page_source, "html.parser")

    def setUp(self):
        self.user = UserFactory(username="my_regularuser@example.com")

        self.browser.get(f"{self.live_server_url}/assignments/")
        WebDriverWait(self.browser, 60).until(
            EC.presence_of_element_located((By.CLASS_NAME, "btn-toolbar"))
        )
        self.soup = BeautifulSoup(self.browser.page_source, "html.parser")

    def test_new_link(self):
        self.user.user_permissions.add(
            get_permission(DeviceAssignment, "view_deviceassignment")
        )
        self.user.save()


class DeviceAssignmentListWithPermissionTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        UserFactory(username="my_regularuser@example.com")
        DeviceAssignmentFactory(id=1)

    def setUp(self):
        self.user = User.objects.get(username="my_regularuser@example.com")
        self.client.force_login(self.user)
        self.user.user_permissions.add(
            get_permission(DeviceAssignment, "view_deviceassignment")
        )

    def test_new_link(self):
        self.user.user_permissions.add(
            get_permission(DeviceAssignment, "add_deviceassignment")
        )
        self.response = self.client.get(reverse("assignments:index"))
        self.assertInHTML(
            new_link,
            self.response.content.decode(),
        )

    def test_quickassign_link(self):
        self.user.user_permissions.add(
            get_permission(DeviceAssignment, "add_deviceassignment")
        )
        self.response = self.client.get(reverse("assignments:index"))
        self.assertInHTML(
            new_link,
            self.response.content.decode(),
        )
