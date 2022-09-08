from django.test import TestCase
from django.urls import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from authentication.tests.factories import SuperuserUserFactory, User, UserFactory
from assignments.models import DeviceAssignment
from assignments.tests.factories import DeviceAssignmentFactory
from inventory.tests.helpers import get_permission
from inventory.tests.helpers import get_chrome_driver, chrome_click_element
from seleniumlogin import force_login
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

new_link = '<a class="btn btn-primary m-2" role="button" href="/assignments/new/">Create Assignment</a>'
quickassign_link = '<a class="btn btn-primary m-2" role="button" href="/assignments/quickassign/">Quick Assign</a>'
DEFAULT_LINKS = []
ALL_LINKS = [new_link, quickassign_link]


class DeviceAssignmenListSuperuserTest(TestCase):
    """Checks that the List View loads the appropriate links"""

    @classmethod
    def setUpTestData(cls):
        SuperuserUserFactory(username="my_superuser@example.com")
        DeviceAssignmentFactory(id=1)

    def setUp(self):
        self.user = User.objects.get(username="my_superuser@example.com")
        self.client.force_login(self.user)
        self.response = self.client.get(reverse("assignments:index"))

    def test_default_links_exist(self):
        if len(DEFAULT_LINKS) == 0:
            return
        for link in DEFAULT_LINKS:
            self.assertInHTML(
                link,
                self.response.content.decode(),
            )

    def test_all_links_exist(self):
        if len(ALL_LINKS) == 0:
            return
        for link in ALL_LINKS:
            self.assertInHTML(
                link,
                self.response.content.decode(),
            )

    def test_template_used(self):
        self.assertTemplateUsed(self.response, "assignments/deviceassignment_list.html")
        self.assertTemplateUsed(self.response, "dashboard/dashboard.html")
        self.assertTemplateUsed(self.response, "partials/datatables.html")

    def test_title(self):
        self.assertInHTML("Inventory - Assignments", self.response.content.decode())


class DeviceAssignmentListWithoutPermissionTest(TestCase):
    """
    Checks that the Detail List loads the appropriate links
    when the user only has permission to view devices
    """

    @classmethod
    def setUpTestData(cls):
        UserFactory(username="my_regularuser@example.com")
        DeviceAssignmentFactory(id=1)

    def setUp(self):
        self.user = User.objects.get(username="my_regularuser@example.com")
        self.client.force_login(self.user)
        self.response = self.client.get(reverse("assignments:index"))

    def test_new_link(self):
        self.assertNotIn(
            new_link,
            self.response.content.decode(),
        )


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


class DeviceAssignmentLiveTest(StaticLiveServerTestCase):
    def get_element(self, locator):
        return WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located(locator)
        )

    def setUp(self):
        self.browser = get_chrome_driver()
        superuser = SuperuserUserFactory()
        force_login(superuser, self.browser, f"{self.live_server_url}/")
        self.assignment = DeviceAssignmentFactory()
        self.browser.get(f"{self.live_server_url}/assignments/")
        self.assignment_row = self.get_element(
            (
                By.XPATH,
                f'//*[@id="assignment_list"]/tbody/tr[@id="deviceassignment_{self.assignment.id}"]',
            )
        )

    def test_action_column_header(self):
        actions_header = self.get_element(
            (
                By.XPATH,
                '//*[@id="assignment_list"]/thead/tr/th//*[normalize-space(text()) = "Action"]',
            )
        )
        self.assertEqual(
            actions_header.text,
            "Action",
            msg="Action header found does not say 'Action'",
        )

    def test_action_view_button(self):
        url = f"/assignments/{self.assignment.id}/"
        view_button = self.assignment_row.find_element(
            by=By.XPATH, value=f'//a[@href="{url}"]'
        )
        self.assertIn(
            "btn-primary",
            view_button.get_attribute("class"),
            msg="view button missing class 'btn-primary'",
        )
        self.assertIn(
            "btn",
            view_button.get_attribute("class"),
            msg="view button missing class 'btn'",
        )

    def test_action_edit_button(self):
        url = f"/assignments/{self.assignment.id}/edit/"
        edit_button = self.assignment_row.find_element(
            by=By.XPATH, value=f'//a[@href="{url}"]'
        )
        self.assertIn(
            "btn-secondary",
            edit_button.get_attribute("class"),
            msg="edit button missing class 'btn-primary'",
        )
        self.assertIn(
            "btn",
            edit_button.get_attribute("class"),
            msg="edit button missing class 'btn'",
        )

    def test_action_turnin_button(self):
        url = f"/assignments/{self.assignment.id}/turnin/"
        turnin_button = self.assignment_row.find_element(
            by=By.XPATH, value=f'//a[@href="{url}"]'
        )
        self.assertIn(
            "btn-success",
            turnin_button.get_attribute("class"),
            msg="turnin button missing class 'btn-success'",
        )
        self.assertIn(
            "btn",
            turnin_button.get_attribute("class"),
            msg="turnin button missing class 'btn'",
        )

    def test_action_delete_button(self):
        url = f"/assignments/{self.assignment.id}/delete/"
        delete_button = self.assignment_row.find_element(
            by=By.XPATH, value=f'//a[@href="{url}"]'
        )
        self.assertIn(
            "btn-danger",
            delete_button.get_attribute("class"),
            msg="delete button missing class 'btn-danger'",
        )
        self.assertIn(
            "btn",
            delete_button.get_attribute("class"),
            msg="delete button missing class 'btn'",
        )
