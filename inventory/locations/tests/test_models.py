from django.test import TestCase
from django.db.models import UniqueConstraint

from locations.models import Building, Room
from .factories import BuildingFactory, RoomFactory


class BuildingModelTest(TestCase):
    def setUp(self):
        BuildingFactory(id=1)

    def test_name_label(self):
        building = Building.objects.get(id=1)
        field_label = building._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")

    def test_name_max_length(self):
        building = Building.objects.get(id=1)
        max_length = building._meta.get_field("name").max_length
        self.assertEqual(max_length, 255)

    def test_name_unique(self):
        building = Building.objects.get(id=1)
        unique = building._meta.get_field("name").unique
        self.assertTrue(unique)

    def test_internal_id_label(self):
        building = Building.objects.get(id=1)
        field_label = building._meta.get_field("internal_id").verbose_name
        self.assertEqual(field_label, "internal id")

    def test_internal_id_max_length(self):
        building = Building.objects.get(id=1)
        max_length = building._meta.get_field("internal_id").max_length
        self.assertEqual(max_length, 255)

    def test_internal_id_unique(self):
        building = Building.objects.get(id=1)
        unique = building._meta.get_field("internal_id").unique
        self.assertTrue(unique)

    def test_acronym_label(self):
        building = Building.objects.get(id=1)
        field_label = building._meta.get_field("acronym").verbose_name
        self.assertEqual(field_label, "acronym")

    def test_acronym_max_length(self):
        building = Building.objects.get(id=1)
        max_length = building._meta.get_field("acronym").max_length
        self.assertEqual(max_length, 255)

    def test_acronym_not_unique(self):
        building = Building.objects.get(id=1)
        unique = building._meta.get_field("acronym").unique
        self.assertFalse(unique)

    def test_active_label(self):
        building = Building.objects.get(id=1)
        field_label = building._meta.get_field("active").verbose_name
        self.assertEqual(field_label, "active")

    ### Functions ###
    def test___str__(self):
        building = BuildingFactory(name="test_name")
        self.assertEqual(building.__str__(), f"{building.name}")


class RoomModelTest(TestCase):
    @classmethod
    def setUpTestData(self):
        RoomFactory(id=1)

    def setUp(self):
        self.room = Room.objects.get(id=1)

    def test_room_label(self):
        field_label = self.room._meta.get_field("number").verbose_name
        self.assertEqual(field_label, "number")

    def test_room_max_length(self):
        max_length = self.room._meta.get_field("number").max_length
        self.assertEqual(max_length, 255)

    def test_building_foreign_key(self):
        self.assertEqual(self.room._meta.get_field("building").related_model, Building)

    def test_room_unique_by_building(self):
        constraints = self.room._meta.constraints
        unique_by_building_constraint = list(
            filter(
                lambda constraint: constraint.name == "unique_room_per_building",
                constraints,
            )
        )
        self.assertEqual(len(unique_by_building_constraint), 1)
        # Asserts all values are the same in both lists regardless of order
        self.assertCountEqual(
            unique_by_building_constraint[0].fields,
            (
                "building",
                "number",
            ),
        )

    def test_unique_constraints(self):
        expected_constraint_fields = [
            (
                "number",
                "building",
            )
        ]
        constraints = [
            c for c in Room._meta.constraints if isinstance(c, UniqueConstraint)
        ]
        self.assertEqual(
            len(expected_constraint_fields),
            len(constraints),
            "Difference in unique constraint length.",
        )
        for constraint in constraints:
            self.assertIn(constraint.fields, expected_constraint_fields)

    ### Functions ###
    def test___str__(self):
        building = BuildingFactory(name="test_building_name")
        room = RoomFactory(number="test_room_name", building=building)
        self.assertEqual(room.__str__(), f"{building.name} Room {room.number}")
