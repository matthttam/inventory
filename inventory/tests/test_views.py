from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

from authentication.tests.decorators import assert_redirect_to_login
from inventory.tests.helpers import get_permission
from authentication.tests.factories import UserFactory
from people.tests.factories import PersonFactory
from devices.tests.factories import DeviceFactory
from assignments.models import DeviceAssignment


class JSONResponseMixinTest(TestCase):
    pass


class JSONListViewTest(TestCase):
    pass


class JSONFormViewTest(TestCase):
    pass


class InventoryAboutViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        UserFactory(id=1)

    def setUp(self):
        self.user = User.objects.get(id=1)
        self.client.force_login(self.user)

    def test_about(self):
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "about.html")
