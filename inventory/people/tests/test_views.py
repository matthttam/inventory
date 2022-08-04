from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from authentication.tests.decorators import assert_redirect_to_login
from authentication.tests.factories import UserFactory

from inventory.tests.helpers import get_permission
from people.models import Person
from people.tests.factories import PersonFactory, PersonStatusFactory, PersonTypeFactory


class PersonListViewAuthenticatedWithPermissionTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        UserFactory(id=1)

    def setUp(self):
        self.user = User.objects.get(id=1)
        self.client.force_login(self.user)
        self.user.user_permissions.add(get_permission(Person, "view_person"))

    def test_no_people(self):
        response = self.client.get(reverse("people:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "people/person_list.html")

    def test_one_person(self):
        device_assignment = PersonFactory(id=1)
        response = self.client.get(reverse("people:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "people/person_list.html")

    def test_ten_people(self):
        device_people = PersonFactory.create_batch(10)
        response = self.client.get(reverse("people:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "people/person_list.html")


class PersonDetailViewAuthenticatedWithPermissionTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        UserFactory(id=1)

    def setUp(self):
        self.user = User.objects.get(id=1)
        self.client.force_login(self.user)
        self.user.user_permissions.add(get_permission(Person, "view_person"))

    def test_invalid_person(self):
        response = self.client.get(reverse("people:detail", args=[1]))
        self.assertEqual(response.status_code, 404)

    def test_valid_person(self):
        person = PersonFactory(first_name="TestName123")
        response = self.client.get(reverse("people:detail", args=[person.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "people/person_detail.html")
        self.assertTemplateUsed(response, "people/partials/person_auditlog.html")
        self.assertContains(response, "TestName123")
        self.assertEqual(response.context["person"], person)


class PersonUpdateViewAuthenticatedWithPermissionTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        UserFactory(id=1)

    def setUp(self):
        self.user = User.objects.get(id=1)
        self.client.force_login(self.user)
        self.user.user_permissions.add(get_permission(Person, "change_person"))

    def test_invalid_person(self):
        response = self.client.get(reverse("people:edit", args=[1]))
        self.assertEqual(response.status_code, 404)

    def test_valid_person(self):
        person = PersonFactory(id=1)
        response = self.client.get(reverse("people:edit", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "people/person_form.html")


class PersonCreateViewAuthenticatedWithPermissionTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        UserFactory(id=1)

    def setUp(self):
        self.user = User.objects.get(id=1)
        self.client.force_login(self.user)
        self.user.user_permissions.add(
            get_permission(Person, "add_person"),
            get_permission(Person, "view_person"),
        )

    def test_new_person(self):
        response = self.client.get(reverse("people:new"))
        self.assertEqual(response.status_code, 200)

    def test_new_person_post(self):
        type = PersonTypeFactory(name="Staff")
        status = PersonStatusFactory(name="Active")
        person = PersonFactory.build(id=1)
        person_dict = {
            "first_name": person.first_name,
            "middle_name": person.middle_name,
            "last_name": person.last_name,
            "email": person.email,
            "internal_id": person.internal_id,
            "type": type.id,
            "status": status.id,
            "google_id": "",
        }
        response = self.client.post(reverse("people:new"), person_dict)
        person_object = Person.objects.get(internal_id=person_dict['internal_id'])
        self.assertIsNotNone(person_object)
        self.assertEqual(person_object.id, person.id)
        self.assertRedirects(
            response,
            reverse("people:detail", kwargs={"pk": person_object.pk}),
            status_code=302,
        )


class PersonDeleteViewAuthenticatedWithPermissionTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        UserFactory(id=1)
        PersonFactory(id=1)

    def setUp(self):
        self.user = User.objects.get(id=1)
        self.device_assignment = Person.objects.get(id=1)
        self.client.force_login(self.user)
        self.user.user_permissions.add(get_permission(Person, "delete_person"))
        self.user.user_permissions.add(get_permission(Person, "view_person"))

    def test_delete_person(self):
        response = self.client.get(reverse("people:delete", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "people/person_confirm_delete.html")

    def test_delete_person_post(self):

        response = self.client.post(reverse("people:delete", args=[1]))
        self.assertRedirects(response, reverse("people:index"))
        device_people = Person.objects.filter(id=1)
        self.assertEqual(len(device_people), 0)


class PersonViewUnauthenticatedTest(TestCase):
    @assert_redirect_to_login(reverse("people:index"))
    def test_device_assignment_list_redirects_to_login(self):
        pass

    @assert_redirect_to_login(reverse("people:detail", args=[1]))
    def test_device_assignment_detail_redirects_to_login(self):
        pass

    @assert_redirect_to_login(reverse("people:edit", args=[1]))
    def test_device_assignment_update_redirects_to_login(self):
        pass

    @assert_redirect_to_login(reverse("people:new"))
    def test_device_assignment_create_redirects_to_login(self):
        pass

    @assert_redirect_to_login(reverse("people:delete", args=[1]))
    def test_device_assignment_delete_redirects_to_login(self):
        pass


class PersonViewsAuthenticatedWithoutPermissionTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        UserFactory(id=1)

    def setUp(self):
        self.user = User.objects.get(id=1)
        self.client.force_login(self.user)

    def test_device_assignment_list_redirects_to_login(self):
        response = self.client.get(reverse("people:index"))
        self.assertEqual(response.status_code, 403)

    def test_device_assignment_detail_redirects_to_login(self):
        response = self.client.get(reverse("people:detail", args=[1]))
        self.assertEqual(response.status_code, 403)

    def test_device_assignment_update_redirects_to_login(self):
        response = self.client.get(reverse("people:edit", args=[1]))
        self.assertEqual(response.status_code, 403)

    def test_device_assignment_create_redirects_to_login(self):
        response = self.client.get(reverse("people:new"))
        self.assertEqual(response.status_code, 403)

    def test_device_assignment_delete_redirects_to_login(self):
        response = self.client.get(reverse("people:delete", args=[1]))
        self.assertEqual(response.status_code, 403)
