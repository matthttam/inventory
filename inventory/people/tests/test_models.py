from datetime import datetime
from zoneinfo import ZoneInfo
from django.utils import timezone
from django.test import TestCase
from people.models import Person, PersonManager, PersonType, PersonStatus
from .factories import (
    PersonFactory,
    PersonWithBuildingsFactory,
    PersonWithRoomsFactory,
    PersonStatusFactory,
    PersonTypeFactory,
)
from locations.tests.factories import BuildingFactory
from locations.models import Building, Room
from assignments.tests.factories import (
    DeviceAssignmentFactory,
    DeviceAssignmentWithReturnDatetimeFactory,
)

tz = ZoneInfo(timezone.settings.TIME_ZONE)


class PersonTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        PersonFactory(id=1)

    def setUp(self):
        self.person = Person.objects.get(id=1)

    def test_first_name_label(self):
        field_label = self.person._meta.get_field("first_name").verbose_name
        self.assertEqual(field_label, "first name")

    def test_first_name_max_length(self):
        max_length = self.person._meta.get_field("first_name").max_length
        self.assertEqual(max_length, 255)

    def test_middle_name_label(self):
        field_label = self.person._meta.get_field("middle_name").verbose_name
        self.assertEqual(field_label, "middle name")

    def test_middle_name_max_length(self):
        max_length = self.person._meta.get_field("middle_name").max_length
        self.assertEqual(max_length, 255)

    def test_last_name_label(self):
        field_label = self.person._meta.get_field("last_name").verbose_name
        self.assertEqual(field_label, "last name")

    def test_last_name_max_length(self):
        max_length = self.person._meta.get_field("last_name").max_length
        self.assertEqual(max_length, 255)

    def test_email_unique(self):
        unique = self.person._meta.get_field("email").unique
        self.assertTrue(unique)

    def test_internal_id_label(self):
        field_label = self.person._meta.get_field("internal_id").verbose_name
        self.assertEqual(field_label, "internal id")

    def test_internal_id_max_length(self):
        max_length = self.person._meta.get_field("internal_id").max_length
        self.assertEqual(max_length, 255)

    def test_internal_id_unique(self):
        unique = self.person._meta.get_field("internal_id").unique
        self.assertTrue(unique)

    def test_type_foreign_key(self):
        self.assertEqual(self.person._meta.get_field("type").related_model, PersonType)

    def test_status_foreign_key(self):
        self.assertEqual(
            self.person._meta.get_field("status").related_model, PersonStatus
        )

    def test_buildings_foreign_key(self):
        self.assertEqual(
            self.person._meta.get_field("buildings").related_model, Building
        )

    def test_rooms_foreign_key(self):
        self.assertEqual(self.person._meta.get_field("rooms").related_model, Room)

    def test_post_save_signal(self):
        self.skipTest("Need to test")

    def test_objects_is_instance_of_person_manager(self):
        self.assertIsInstance(Person.objects, PersonManager)

    ### Properties ###
    def test_display_name(self):
        person = PersonFactory(first_name="Mark", last_name="Twain")
        self.assertEqual(person.display_name, f"{person.first_name} {person.last_name}")

    def test_building_list(self):
        person = Person.objects.get(id=1)
        person.buildings.set([BuildingFactory(name="z"), BuildingFactory(name="a")])
        person = Person.objects.get(id=1)
        self.assertEqual(person.building_list, "a, z")
        self.assertNotEqual(person.building_list, "z, a")

    ### Functions ###
    def test___str__(self):
        person = PersonFactory(
            first_name="Joe", last_name="Schmoe", internal_id="unique_id-1234"
        )
        self.assertEqual(
            person.__str__(),
            f"{person.first_name} {person.last_name} ({person.internal_id})",
        )

    def test_get_absolute_url(self):
        person = Person.objects.get(id=1)
        self.assertEqual(person.get_absolute_url(), "/people/1/")

    ### Test custom model queryset
    def test_outstanding_assignment_count(self):
        person = Person.objects.get(id=1)
        self.assertEqual(person.outstanding_assignment_count, 0)
        DeviceAssignmentFactory(person=person, return_datetime=None)
        person = Person.objects.get(id=1)
        self.assertEqual(person.outstanding_assignment_count, 1)

    def test_has_outstanding_assignment(self):
        person = Person.objects.get(id=1)
        self.assertFalse(person.has_outstanding_assignment)
        DeviceAssignmentWithReturnDatetimeFactory(person=person, return_datetime=None)
        person = Person.objects.get(id=1)
        self.assertTrue(person.has_outstanding_assignment)
        person.deviceassignment_set.update(return_datetime=datetime.now(tz=tz))
        person = Person.objects.get(id=1)
        self.assertFalse(person.has_outstanding_assignment)

    def test_is_active(self):
        active_status = PersonStatusFactory(name="Active", is_inactive=False)
        inactive_status = PersonStatusFactory(name="Inctive", is_inactive=True)
        PersonFactory(email="testuser@example.com", status=active_status)
        person = Person.objects.get(email="testuser@example.com")
        self.assertTrue(person.is_active)
        person.status = inactive_status
        person.save()
        person = Person.objects.get(email="testuser@example.com")
        self.assertFalse(person.is_active)


class PersonWithBuildingsTest(TestCase):
    def setUp(self):
        PersonWithBuildingsFactory(id=1)

    def test_buildings_many_to_many(self):
        person = Person.objects.get(id=1)
        buildings_length = len(person.buildings.all())
        self.assertGreater(buildings_length, 0)


class PersonWithRoomsTest(TestCase):
    def setUp(self):
        PersonWithRoomsFactory(id=1)

    def test_rooms_many_to_many(self):
        person = Person.objects.get(id=1)
        rooms_length = len(person.rooms.all())
        self.assertGreater(rooms_length, 0)


class PersonTypeTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        PersonTypeFactory(id=1)

    def setUp(self):
        self.person = PersonType.objects.get(id=1)

    def test_name_label(self):
        field_label = self.person._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")

    def test_name_max_length(self):
        max_length = self.person._meta.get_field("name").max_length
        self.assertEqual(max_length, 255)

    def test___str__(self):
        person_type = PersonTypeFactory(name="test_person_type")
        self.assertEqual(person_type.__str__(), person_type.name)


class PersonStatusTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        PersonStatusFactory(id=1)

    def setUp(self):
        self.person = PersonStatus.objects.get(id=1)

    def test_verbose_name_plural(self):
        field_label_plural = PersonStatus._meta.verbose_name_plural
        self.assertEqual(field_label_plural, "Person statuses")

    def test_name_label(self):
        field_label = self.person._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")

    def test_name_max_length(self):
        max_length = self.person._meta.get_field("name").max_length
        self.assertEqual(max_length, 255)

    ### Functions ###
    def test___str__(self):
        person = PersonStatusFactory(name="test_person_status")
        self.assertEqual(person.__str__(), f"{person.name}")
