from assignments.tests.factories import DeviceAssignmentFactory
from authentication.tests.factories import SuperuserUserFactory, User
from bs4 import BeautifulSoup
from django.test import TestCase
from django.urls import reverse


class DeviceAssignmentListTemplateTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        SuperuserUserFactory(username="my_superuser@example.com")
        DeviceAssignmentFactory(id=1)

    def setUp(self):
        self.user = User.objects.get(username="my_superuser@example.com")
        self.client.force_login(self.user)
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


# class DeviceAssignmentListSuperuserLiveTest(StaticLiveServerTestCase):
#    """Checks that the List View loads the appropriate links"""
#
#    @classmethod
#    def setUpClass(cls):
#        super().setUpClass()
#        cls.browser = get_chrome_driver()
#        SuperuserUserFactory(username="my_superuser@example.com")
#        cls.user = User.objects.get(username="my_superuser@example.com")
#        force_login(cls.user, cls.browser, f"{cls.live_server_url}/")
#        DeviceAssignmentFactory(id=1)
#        cls.browser.get(f"{cls.live_server_url}/assignments/")
#        WebDriverWait(cls.browser, 60).until(
#            EC.presence_of_element_located((By.CLASS_NAME, "btn-toolbar"))
#        )
#        cls.soup = BeautifulSoup(cls.browser.page_source, "html.parser")
#
#    @classmethod
#    def tearDownClass(cls):
#        #cls.browser.quit()
#        super().tearDownClass()
#
#    def test_action_header(self):
#        action_header = self.soup.find("th", string="Action")
#        self.assertIsNotNone(action_header)
#
#    def test_view_link_exists(self):
#        view_link = self.soup.select_one('a[href="/assignments/1/"]')
#        self.assertIsNotNone(view_link)
#
#    def test_edit_link_exists(self):
#        edit_link = self.soup.select_one('a[href="/assignments/1/edit/"]')
#        self.assertIsNotNone(edit_link)
#
#    def test_turnin_link_exists(self):
#        turnin_link = self.soup.select_one('a[href="/assignments/1/turnin/"]')
#        self.assertIsNotNone(turnin_link)
#
#    def test_delete_link_exists(self):
#        delete_link = self.soup.select_one('a[href="/assignments/1/delete/"]')
#        self.assertIsNotNone(delete_link)


##class DeviceAssignmentListWithViewPermissionLiveTest(StaticLiveServerTestCase):
##    """
##    Checks that the Detail List loads the appropriate links
##    when the user only has permission to view devices
##    """
##
##    @classmethod
##    def setUpClass(cls):
##        super().setUpClass()
##        cls.browser = get_chrome_driver()
##        UserFactory(
##            username="view_user@example.com",
##            user_permissions=[
##                (DeviceAssignment, "view_deviceassignment"),
##            ],
##        )
##        cls.user = User.objects.get(username="view_user@example.com")
##        force_login(cls.user, cls.browser, f"{cls.live_server_url}/")
##        DeviceAssignmentFactory()
##        cls.browser.get(f"{cls.live_server_url}/assignments/")
##        WebDriverWait(cls.browser, 60).until(
##            EC.presence_of_element_located((By.CLASS_NAME, "btn-toolbar"))
##        )
##        cls.soup = BeautifulSoup(cls.browser.page_source, "html.parser")
##
##    @classmethod
##    def tearDownClass(cls):
##        # cls.browser.quit()
##        super().tearDownClass()
##
##    # def _fixture_setup(self):
##    # pass
##
##    def test_view_link_exists(self):
##        view_link = self.soup.select_one('a[href="/assignments/1/"]')
##        self.assertIsNotNone(view_link)
##
##    def test_edit_link_missing(self):
##        edit_link = self.soup.select_one('a[href="/assignments/1/edit/"]')
##        self.assertIsNone(edit_link)
##
##    def test_turnin_link_missing(self):
##        turnin_link = self.soup.select_one('a[href="/assignments/1/turnin/"]')
##        self.assertIsNone(turnin_link)
##
##    def test_delete_link_missing(self):
##        delete_link = self.soup.select_one('a[href="/assignments/1/delete/"]')
##        self.assertIsNone(delete_link)
##
##
##class DeviceAssignmentListWithEditPermissionLiveTest(StaticLiveServerTestCase):
##    """
##    Checks that the Detail List loads the appropriate links
##    when the user only has permission to view devices
##    """
##
##    @classmethod
##    def setUpClass(cls):
##        super().setUpClass()
##        cls.browser = get_chrome_driver()
##        UserFactory(
##            username="edit_user@example.com",
##            user_permissions=[
##                (DeviceAssignment, "view_deviceassignment"),
##                (DeviceAssignment, "change_deviceassignment"),
##            ],
##        )
##        cls.user = User.objects.get(username="edit_user@example.com")
##        force_login(cls.user, cls.browser, f"{cls.live_server_url}/")
##        DeviceAssignmentFactory()
##        cls.browser.get(f"{cls.live_server_url}/assignments/")
##        WebDriverWait(cls.browser, 60).until(
##            EC.presence_of_element_located((By.CLASS_NAME, "btn-toolbar"))
##        )
##        cls.soup = BeautifulSoup(cls.browser.page_source, "html.parser")
##
##    @classmethod
##    def tearDownClass(cls):
##        # cls.browser.quit()
##        super().tearDownClass()
##
##    def test_view_link_exists(self):
##        view_link = self.soup.select_one('a[href="/assignments/1/"]')
##        self.assertIsNotNone(view_link)
##
##    def test_edit_link_exists(self):
##        edit_link = self.soup.select_one('a[href="/assignments/1/edit/"]')
##        self.assertIsNotNone(edit_link)#
#
#    def test_turnin_link_missing(self):
#        turnin_link = self.soup.select_one('a[href="/assignments/1/turnin/"]')
#        self.assertIsNone(turnin_link)#
#
#    def test_delete_link_missing(self):
#        delete_link = self.soup.select_one('a[href="/assignments/1/delete/"]')
#        self.assertIsNone(delete_link)#
#
#
# class DeviceAssignmentListWithTurninPermissionLiveTest(StaticLiveServerTestCase):
#    """
#    Checks that the Detail List loads the appropriate links
#    when the user only has permission to view devices
#    """#
#
#    @classmethod
#    def setUpClass(cls):
#        super().setUpClass()
#        cls.browser = get_chrome_driver()
#        UserFactory(
#            username="turnin_user@example.com",
#            user_permissions=[
#                (DeviceAssignment, "view_deviceassignment"),
#                (DeviceAssignment, "turnin_deviceassignment"),
#            ],
#        )
#        cls.user = User.objects.get(username="turnin_user@example.com")
#        force_login(cls.user, cls.browser, f"{cls.live_server_url}/")
#        DeviceAssignmentFactory()
#        cls.browser.get(f"{cls.live_server_url}/assignments/")
#        WebDriverWait(cls.browser, 60).until(
#            EC.presence_of_element_located((By.CLASS_NAME, "btn-toolbar"))
#        )
#        cls.soup = BeautifulSoup(cls.browser.page_source, "html.parser")#
#
#    @classmethod
#    def tearDownClass(cls):
#        # cls.browser.quit()
#        super().tearDownClass()#
#
#    def test_view_link_exists(self):
#        view_link = self.soup.select_one('a[href="/assignments/1/"]')
#        self.assertIsNotNone(view_link)#
#
#    def test_edit_link_missing(self):
#        edit_link = self.soup.select_one('a[href="/assignments/1/edit/"]')
#        self.assertIsNone(edit_link)#
#
#    def test_turnin_link_exists(self):
#        turnin_link = self.soup.select_one('a[href="/assignments/1/turnin/"]')
#        self.assertIsNotNone(turnin_link)#
#
#    def test_delete_link_missing(self):
#        delete_link = self.soup.select_one('a[href="/assignments/1/delete/"]')
#        self.assertIsNone(delete_link)#
#
#
# class DeviceAssignmentListWithDeletePermissionLiveTest(StaticLiveServerTestCase):
#    """
#    Checks that the Detail List loads the appropriate links
#    when the user only has permission to view devices
#    """
#
#    @classmethod
#    def setUpClass(cls):
#        super().setUpClass()
#        cls.browser = get_chrome_driver()
#        UserFactory(
#            username="delete_user@example.com",
#            user_permissions=[
#                (DeviceAssignment, "view_deviceassignment"),
#                (DeviceAssignment, "delete_deviceassignment"),
#            ],
#        )
#        cls.user = User.objects.get(username="delete_user@example.com")
#        force_login(cls.user, cls.browser, f"{cls.live_server_url}/")
#        DeviceAssignmentFactory()
#        cls.browser.get(f"{cls.live_server_url}/assignments/")
#        WebDriverWait(cls.browser, 60).until(
#            EC.presence_of_element_located((By.CLASS_NAME, "btn-toolbar"))
#        )
#        cls.soup = BeautifulSoup(cls.browser.page_source, "html.parser")
#
#    @classmethod
#    def tearDownClass(cls):
#        # cls.browser.quit()
#        super().tearDownClass()
#
#    def test_view_link_exists(self):
#        view_link = self.soup.select_one('a[href="/assignments/1/"]')
#        self.assertIsNotNone(view_link)
#
#    def test_edit_link_missing(self):
#        edit_link = self.soup.select_one('a[href="/assignments/1/edit/"]')
#        self.assertIsNone(edit_link)
#
#    def test_turnin_link_missing(self):
#        turnin_link = self.soup.select_one('a[href="/assignments/1/turnin/"]')
#        self.assertIsNone(turnin_link)
#
#    def test_delete_link_exists(self):
#        delete_link = self.soup.select_one('a[href="/assignments/1/delete/"]')
#        self.assertIsNotNone(delete_link)
#
