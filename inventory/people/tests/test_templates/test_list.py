from django.test import TestCase
from django.urls import reverse
from authentication.tests.factories import SuperuserUserFactory, User
from people.tests.factories import PersonFactory


class PersonListSuperuserTest(TestCase):
    """Checks that the List View loads the appropriate links"""

    @classmethod
    def setUpTestData(cls):
        SuperuserUserFactory(username="my_superuser@example.com")
        PersonFactory(id=1)

    def setUp(self):
        self.user = User.objects.get(username="my_superuser@example.com")
        self.client.force_login(self.user)
        self.response = self.client.get(reverse("people:index"))

    def test_template_used(self):
        self.assertTemplateUsed(self.response, "people/person_list.html")
        self.assertTemplateUsed(self.response, "dashboard/dashboard.html")
        self.assertTemplateUsed(self.response, "partials/datatables_css.html")
        self.assertTemplateUsed(self.response, "partials/datatables_js.html")

    def test_title(self):
        self.assertInHTML("Inventory - People", self.response.content.decode())
