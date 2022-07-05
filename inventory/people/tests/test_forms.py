from django.test import TestCase
from people.forms import PersonForm
from django.forms.models import model_to_dict
from people.tests.factories import PersonFactory, PersonStatusFactory, PersonTypeFactory
from people.models import PersonStatus, PersonType
from devices.models import DeviceModel
from locations.models import Building, Room


class PersonFormTest(TestCase):
    def test_valid_form(self):
        person_status = PersonStatusFactory(name="status")
        person_type = PersonTypeFactory(name="type")
        person = PersonFactory.build(status=person_status, type=person_type)

        form = PersonForm(
            data=model_to_dict(
                person,
                fields=[
                    "internal_id",
                    "first_name",
                    "middle_name",
                    "last_name",
                    "email",
                    "type",
                    "status",
                ],
            )
        )
        print(form.errors)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.errors, {})
        self.assertQuerysetEqual(
            form.fields["status"].queryset,
            PersonStatus.objects.all(),
            ordered=False,
        )
        self.assertQuerysetEqual(
            form.fields["type"].queryset,
            PersonType.objects.all(),
            ordered=False,
        )

    def test_invalid_form(self):
        person_status = PersonStatusFactory(name="status")
        person_type = PersonTypeFactory(name="type")
        person = PersonFactory(status=person_status, type=person_type)

        form = PersonForm(
            data=model_to_dict(
                person,
                fields=[
                    "internal_id",
                    "first_name",
                    "middle_name",
                    "last_name",
                    "email",
                    "type",
                    "status",
                ],
            )
        )

        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors.keys())
        self.assertIn("Person with this Email already exists.", form.errors["email"][0])
        self.assertIn("internal_id", form.errors.keys())
        self.assertIn(
            "Person with this Internal id already exists.",
            form.errors["internal_id"][0],
        )
