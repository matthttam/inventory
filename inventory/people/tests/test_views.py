from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from authentication.tests.decorators import assert_redirect_to_login
from authentication.tests.factories import UserFactory

from inventory.tests.helpers import get_permission
from people.models import Person
from people.tests.factories import PersonFactory, PersonStatusFactory, PersonTypeFactory
from people.views import PersonDatatableServerSideProcessingView
from django.core.exceptions import FieldError
import json
from unittest.mock import Mock, patch, ANY
from django.core.handlers.wsgi import WSGIRequest


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
        PersonFactory()
        response = self.client.get(reverse("people:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "people/person_list.html")

    def test_ten_people(self):
        PersonFactory.create_batch(10)
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
        person_object = Person.objects.get(internal_id=person_dict["internal_id"])
        self.assertIsNotNone(person_object)
        self.assertEqual(person_object.internal_id, person.internal_id)
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
        self.person = Person.objects.get(id=1)
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


class PersonDatatableServerSideProcessingViewAuthenticatedWithPermissionTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        UserFactory(id=1)
        PersonFactory(id=1)

    def setUp(self):
        self.user = User.objects.get(id=1)
        self.person = Person.objects.get(id=1)
        self.client.force_login(self.user)
        self.user.user_permissions.add(get_permission(Person, "view_person"))

    def test_dt_index(self):
        response = self.client.get(reverse("people:dt_index"), self.get_dt_querydata())
        self.assertEqual(response.status_code, 200)

    def test_columns_defined_correctly(self):

        view = PersonDatatableServerSideProcessingView()
        self.assertTrue(isinstance(view.columns, list))
        try:
            returnable_values = view.queryset.values(*view.columns)
        except FieldError:
            self.fail("dt_index view specifies columns not accessible from the queryset!")

    @patch("people.views.render_to_string")
    def test_data_callback_adds_actions(self, mock_render_to_string):
        mock_render_to_string.return_value = "<div>mock_actions_html</div>"
        response = self.client.get(reverse("people:dt_index"), self.get_dt_querydata())
        json_data = json.loads(response.content)
        mock_render_to_string.assert_called_with(
            "people/partials/person_list/table_row_buttons.html",
            context=ANY,
            request=ANY,
        )
        args, kwargs = mock_render_to_string.call_args
        self.assertEqual(kwargs["context"]["person"]["id"], 1)
        self.assertTrue(isinstance(kwargs["request"], WSGIRequest))
        self.assertEqual(
            json_data["data"][0]["actions"],
            mock_render_to_string.return_value,
            msg="actions field not set correctly!",
        )

    def get_dt_querydata(self):
        return {
            "draw": "1",
            "columns[0][data]": "id",
            "columns[0][name]": "",
            "columns[0][searchable]": "true",
            "columns[0][orderable]": "true",
            "columns[0][search][value]": "",
            "columns[0][search][regex]": "false",
            "columns[1][data]": "first_name",
            "columns[1][name]": "",
            "columns[1][searchable]": "true",
            "columns[1][orderable]": "true",
            "columns[1][search][value]": "",
            "columns[1][search][regex]": "false",
            "columns[2][data]": "last_name",
            "columns[2][name]": "",
            "columns[2][searchable]": "true",
            "columns[2][orderable]": "true",
            "columns[2][search][value]": "",
            "columns[2][search][regex]": "false",
            "columns[3][data]": "email",
            "columns[3][name]": "",
            "columns[3][searchable]": "true",
            "columns[3][orderable]": "true",
            "columns[3][search][value]": "",
            "columns[3][search][regex]": "false",
            "columns[4][data]": "internal_id",
            "columns[4][name]": "",
            "columns[4][searchable]": "true",
            "columns[4][orderable]": "true",
            "columns[4][search][value]": "",
            "columns[4][search][regex]": "false",
            "columns[5][data]": "type__name",
            "columns[5][name]": "",
            "columns[5][searchable]": "true",
            "columns[5][orderable]": "true",
            "columns[5][search][value]": "",
            "columns[5][search][regex]": "false",
            "columns[6][data]": "status__name",
            "columns[6][name]": "",
            "columns[6][searchable]": "true",
            "columns[6][orderable]": "true",
            "columns[6][search][value]": "",
            "columns[6][search][regex]": "false",
            "columns[7][data]": "primary_building__name",
            "columns[7][name]": "",
            "columns[7][searchable]": "true",
            "columns[7][orderable]": "true",
            "columns[7][search][value]": "",
            "columns[7][search][regex]": "false",
            "columns[8][data]": "outstanding_assignment_count",
            "columns[8][name]": "",
            "columns[8][searchable]": "true",
            "columns[8][orderable]": "true",
            "columns[8][search][value]": "",
            "columns[8][search][regex]": "false",
            "columns[9][data]": "actions",
            "columns[9][name]": "",
            "columns[9][searchable]": "true",
            "columns[9][orderable]": "false",
            "columns[9][search][value]": "",
            "columns[9][search][regex]": "false",
            "order[0][column]": "0",
            "order[0][dir]": "asc",
            "start": "0",
            "length": "10",
            "search[value]": "",
            "search[regex]": "false",
            "_": "1666703070011",
        }


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

    @assert_redirect_to_login(reverse("people:dt_index"))
    def test_device_assignment_create_redirects_to_login(self):
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

    def test_device_assignment_delete_redirects_to_login(self):
        response = self.client.get(reverse("people:dt_index"))
        self.assertEqual(response.status_code, 403)
