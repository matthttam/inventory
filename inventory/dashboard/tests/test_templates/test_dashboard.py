from django.test import TestCase
from django.urls import reverse
from authentication.tests.factories import UserFactory, SuperuserUserFactory
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from devices.models import Device
from people.models import Person
from assignments.models import DeviceAssignment
from inventory.tests.helpers import get_permission
from django.template import Context, Template
from bs4 import BeautifulSoup
import copy


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
        self.assertTemplateUsed(self.response, "dashboard/partials/dashboard_nav.html")


class DashboardTest(TestCase):
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
