from django.test import TestCase
from django.urls import reverse
from authentication.tests.factories import SuperuserUserFactory, User, UserFactory
from assignments.models import DeviceAssignment
from assignments.tests.factories import DeviceAssignmentFactory
from inventory.tests.helpers import get_permission

list_link = '<a class="btn btn-primary m-2" role="button" href="/assignments/" >Assignment List</a>'
update_link = '<a class="btn btn-primary m-2" role="button" href="/assignments/1/edit/">Edit Assignment</a>'
delete_link = '<a class="btn btn-danger m-2" role="button" href="/assignments/1/delete/">Delete Assignment</a>'

DEFAULT_LINKS = [
    list_link,
    update_link,
    delete_link,
]


class DeviceAssignmentDetailSuperuserTest(TestCase):
    """Checks that the Detail View loads the appropriate links"""

    @classmethod
    def setUpTestData(cls):
        SuperuserUserFactory(username="my_superuser@example.com")
        DeviceAssignmentFactory(id=1)

    def setUp(self):
        self.user = User.objects.get(username="my_superuser@example.com")
        self.client.force_login(self.user)
        self.response = self.client.get(reverse("assignments:detail", args=[1]))

    def test_default_links_exist(self):
        for link in DEFAULT_LINKS:
            self.assertInHTML(
                link,
                self.response.content.decode(),
            )

    def test_all_links_exist(self):
        links = [
            list_link,
            update_link,
            delete_link,
        ]
        for link in links:
            self.assertInHTML(
                link,
                self.response.content.decode(),
            )

    def test_template_used(self):
        self.assertTemplateUsed(
            self.response, "assignments/deviceassignment_detail.html"
        )

    def test_title(self):
        self.assertInHTML(
            "Inventory - Assignment Detail", self.response.content.decode()
        )


class DeviceAssignmentDetailWithoutPermissionTest(TestCase):
    """
    Checks that the Detail View loads the appropriate links
    when the user only has permission to view devices
    """

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
        self.response = self.client.get(reverse("assignments:detail", args=[1]))

    def test_update_link_missing(self):
        self.assertNotIn(
            update_link,
            self.response.content.decode(),
        )

    def test_delete_link_missing(self):
        self.assertNotIn(
            delete_link,
            self.response.content.decode(),
        )

    def test_assignment_link(self):
        self.assertInHTML(
            list_link,
            self.response.content.decode(),
        )


class DeviceAssignmentDetailWithPermissionTest(TestCase):
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

    def test_update_link(self):
        self.user.user_permissions.add(
            get_permission(DeviceAssignment, "change_deviceassignment")
        )
        self.response = self.client.get(reverse("assignments:detail", args=[1]))
        self.assertInHTML(
            update_link,
            self.response.content.decode(),
        )

    def test_delete_link(self):
        self.user.user_permissions.add(
            get_permission(DeviceAssignment, "delete_deviceassignment")
        )
        self.response = self.client.get(reverse("assignments:detail", args=[1]))
        self.assertInHTML(
            delete_link,
            self.response.content.decode(),
        )

    def test_assignment_link(self):
        self.user.user_permissions.add(
            get_permission(DeviceAssignment, "add_deviceassignment")
        )
        self.response = self.client.get(reverse("assignments:detail", args=[1]))
        self.assertInHTML(
            list_link,
            self.response.content.decode(),
        )
