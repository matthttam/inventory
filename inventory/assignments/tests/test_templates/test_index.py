from django.test import TestCase
from django.urls import reverse
from authentication.tests.factories import SuperuserUserFactory, User, UserFactory
from assignments.models import DeviceAssignment
from assignments.tests.factories import DeviceAssignmentFactory
from inventory.tests.helpers import get_permission

new_link = '<a class="btn btn-primary m-2" role="button" href="/assignments/new/">Create Assignment</a>'

DEFAULT_LINKS = []
ALL_LINKS = [new_link]


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
        self.assertTemplateUsed(self.response, "datatables.html")

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

    # def test_update_link_missing(self):
    #    self.assertNotIn(
    #        update_link,
    #        self.response.content.decode(),
    #    )
    #
    # def test_delete_link_missing(self):
    #    self.assertNotIn(
    #        delete_link,
    #        self.response.content.decode(),
    #    )

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

    # def test_update_link(self):
    #    self.user.user_permissions.add(
    #        get_permission(DeviceAssignment, "change_deviceassignment")
    #    )
    #    self.response = self.client.get(reverse("assignments:index"))
    #    self.assertInHTML(
    #        update_link,
    #        self.response.content.decode(),
    #    )
    #
    # def test_delete_link(self):
    #    self.user.user_permissions.add(
    #        get_permission(DeviceAssignment, "delete_deviceassignment")
    #    )
    #    self.response = self.client.get(reverse("assignments:index"))
    #    self.assertInHTML(
    #        delete_link,
    #        self.response.content.decode(),
    #    )

    def test_new_link(self):
        self.user.user_permissions.add(
            get_permission(DeviceAssignment, "add_deviceassignment")
        )
        self.response = self.client.get(reverse("assignments:index"))
        self.assertInHTML(
            new_link,
            self.response.content.decode(),
        )
