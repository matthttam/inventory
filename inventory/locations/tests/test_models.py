from django.test import TestCase
from locations.models import Building, Room
from .factories import BuildingFactory, RoomFactory


class BuildingModelTest(TestCase):
    def setUp(self):
        BuildingFactory()

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
        self.assertEqual(unique, True)

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
        self.assertEqual(unique, True)

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
        self.assertEqual(unique, False)

    def test_active_label(self):
        building = Building.objects.get(id=1)
        field_label = building._meta.get_field("active").verbose_name
        self.assertEqual(field_label, "active")


class RoomModelTest(TestCase):
    def setUp(self):
        RoomFactory()

    def test_room_label(self):
        room = Room.objects.get(id=1)
        field_label = room._meta.get_field("number").verbose_name
        self.assertEqual(field_label, "number")

    def test_room_max_length(self):
        room = Room.objects.get(id=1)
        max_length = room._meta.get_field("number").max_length
        self.assertEqual(max_length, 255)

    def test_building_foreign_key(self):
        room = Room.objects.get(id=1)
        self.assertEqual(room._meta.get_field("building").related_model, Building)
