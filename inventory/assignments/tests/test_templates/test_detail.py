from django.test import TestCase
from django.urls import reverse
from authentication.tests.factories import SuperuserUserFactory, User, UserFactory
from assignments.models import DeviceAssignment
from assignments.tests.factories import DeviceAssignmentFactory
from inventory.tests.helpers import get_permission


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

    def test_template_used(self):
        self.assertTemplateUsed(
            self.response, "assignments/deviceassignment_detail.html"
        )
        self.assertTemplateUsed(
            self.response, "assignments/partials/deviceassignment_infobox.html"
        )
        self.assertTemplateUsed(
            self.response, "assignments/partials/deviceassignment_control_buttons.html"
        )

    def test_title(self):
        self.assertInHTML(
            "Inventory - Assignment Detail", self.response.content.decode()
        )
