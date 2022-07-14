from django.test import TestCase
from devices.models import (
    DeviceAccessory,
    DeviceStatus,
    DeviceManufacturer,
    Device,
    DeviceModel,
)
from locations.models import Room, Building
from .factories import (
    DeviceModelFactory,
    DeviceStatusFactory,
    DeviceManufacturerFactory,
    DeviceFactory,
    DeviceAccessoryFactory,
    DeviceManufacturerFactory,
    DeviceAccessoryWithDeviceModelsFactory,
)


class DeviceStatusTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        DeviceStatusFactory(name="test_status")

    def setUp(self):
        self.device_status = DeviceStatus.objects.get(name="test_status")

    def test_name_label(self):
        field_label = self.device_status._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")

    def test_name_max_length(self):
        max_length = self.device_status._meta.get_field("name").max_length
        self.assertEqual(max_length, 255)

    def test_name_unique(self):
        unique = self.device_status._meta.get_field("name").unique
        self.assertTrue(unique)

    def test___str__(self):
        device = DeviceStatusFactory(name="test_status")
        self.assertEqual(device.__str__(), f"{device.name}")


class DeviceManufacturerTest(TestCase):
    def setUp(self):
        DeviceManufacturerFactory(id=1)

    def test_name_label(self):
        device_manufacturer = DeviceManufacturer.objects.get(id=1)
        field_label = device_manufacturer._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")

    def test_name_max_length(self):
        device_manufacturer = DeviceManufacturer.objects.get(id=1)
        max_length = device_manufacturer._meta.get_field("name").max_length
        self.assertEqual(max_length, 255)

    def test___str__(self):
        device_manufacturer = DeviceManufacturerFactory(name="test_status")
        self.assertEqual(device_manufacturer.__str__(), f"{device_manufacturer.name}")


class DeviceModelTest(TestCase):
    def setUp(self):
        DeviceModelFactory(id=1)

    def test_name_label(self):
        device_model = DeviceModel.objects.get(id=1)
        field_label = device_model._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")

    def test_name_max_length(self):
        device_model = DeviceModel.objects.get(id=1)
        max_length = device_model._meta.get_field("name").max_length
        self.assertEqual(max_length, 255)


class DeviceTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        DeviceFactory(id=1)

    def setUp(self):
        self.device = Device.objects.get(id=1)

    def test_serial_number_label(self):
        field_label = self.device._meta.get_field("serial_number").verbose_name
        self.assertEqual(field_label, "serial number")

    def test_serial_number_max_length(self):
        max_length = self.device._meta.get_field("serial_number").max_length
        self.assertEqual(max_length, 255)

    def test_serial_number_unique(self):
        unique = self.device._meta.get_field("serial_number").unique
        self.assertTrue(unique)

    def test_asset_id_label(self):
        field_label = self.device._meta.get_field("asset_id").verbose_name
        self.assertEqual(field_label, "asset id")

    def test_asset_id_not_required(self):
        self.assertEqual(self.device._meta.get_field("asset_id").blank, True)
        self.assertEqual(self.device._meta.get_field("asset_id").null, False)

    def test_asset_id_max_length(self):
        max_length = self.device._meta.get_field("asset_id").max_length
        self.assertEqual(max_length, 255)

    def test_asset_id_unique(self):
        unique = self.device._meta.get_field("asset_id").unique
        self.assertTrue(unique)

    def test_notes_label(self):
        field_label = self.device._meta.get_field("notes").verbose_name
        self.assertEqual(field_label, "notes")

    def test_notes_max_length(self):
        max_length = self.device._meta.get_field("notes").max_length
        self.assertEqual(max_length, 255)

    def test_notes_optional(self):
        self.assertEqual(self.device._meta.get_field("notes").blank, True)
        self.assertEqual(self.device._meta.get_field("notes").null, False)

    def test_status_label(self):
        field_label = self.device._meta.get_field("status").verbose_name
        self.assertEqual(field_label, "status")

    def test_status_required(self):
        self.assertEqual(self.device._meta.get_field("status").blank, False)
        self.assertEqual(self.device._meta.get_field("status").null, False)

    def test_status_foreign_key(self):
        self.assertEqual(
            self.device._meta.get_field("status").related_model, DeviceStatus
        )

    def test_google_id_label(self):
        field_label = self.device._meta.get_field("google_id").verbose_name
        self.assertEqual(field_label, "google id")

    def test_google_id_max_length(self):
        max_length = self.device._meta.get_field("google_id").max_length
        self.assertEqual(max_length, 255)

    def test_google_id_unique(self):
        unique = self.device._meta.get_field("google_id").unique
        self.assertTrue(unique)

    def test_google_id_optional(self):
        self.assertEqual(self.device._meta.get_field("google_id").blank, True)
        self.assertEqual(self.device._meta.get_field("google_id").null, True)

    def test_google_status_label(self):
        field_label = self.device._meta.get_field("google_status").verbose_name
        self.assertEqual(field_label, "google status")

    def test_google_status_max_length(self):
        max_length = self.device._meta.get_field("google_status").max_length
        self.assertEqual(max_length, 255)

    def test_google_status_optional(self):
        self.assertEqual(self.device._meta.get_field("google_status").blank, True)
        self.assertEqual(self.device._meta.get_field("google_status").null, False)

    def test_google_organization_unit_label(self):
        field_label = self.device._meta.get_field(
            "google_organization_unit"
        ).verbose_name
        self.assertEqual(field_label, "google organization unit")

    def test_google_organization_unit_max_length(self):
        max_length = self.device._meta.get_field("google_organization_unit").max_length
        self.assertEqual(max_length, 255)

    def test_google_organization_unit_optional(self):
        self.assertEqual(
            self.device._meta.get_field("google_organization_unit").blank, True
        )
        self.assertEqual(
            self.device._meta.get_field("google_organization_unit").null, False
        )

    def test_google_enrollment_time_label(self):
        field_label = self.device._meta.get_field("google_enrollment_time").verbose_name
        self.assertEqual(field_label, "google enrollment time")

    def test_google_enrollment_time_optional(self):
        self.assertEqual(
            self.device._meta.get_field("google_enrollment_time").blank, True
        )
        self.assertEqual(
            self.device._meta.get_field("google_enrollment_time").null, True
        )

    def test_google_last_policy_sync_label(self):
        field_label = self.device._meta.get_field(
            "google_last_policy_sync"
        ).verbose_name
        self.assertEqual(field_label, "google last policy sync")

    def test_google_last_policy_sync_optional(self):
        self.assertEqual(
            self.device._meta.get_field("google_last_policy_sync").blank, True
        )
        self.assertEqual(
            self.device._meta.get_field("google_last_policy_sync").null, True
        )

    def test_google_location_label(self):
        field_label = self.device._meta.get_field("google_location").verbose_name
        self.assertEqual(field_label, "google location")

    def test_google_location_max_length(self):
        max_length = self.device._meta.get_field("google_location").max_length
        self.assertEqual(max_length, 255)

    def test_google_location_optional(self):
        self.assertEqual(self.device._meta.get_field("google_location").blank, True)
        self.assertEqual(self.device._meta.get_field("google_location").null, False)

    def test_google_most_recent_user_label(self):
        field_label = self.device._meta.get_field(
            "google_most_recent_user"
        ).verbose_name
        self.assertEqual(field_label, "google most recent user")

    def test_google_most_recent_user_max_length(self):
        max_length = self.device._meta.get_field("google_most_recent_user").max_length
        self.assertEqual(max_length, 255)

    def test_google_most_recent_user_optional(self):
        self.assertEqual(
            self.device._meta.get_field("google_most_recent_user").blank, True
        )
        self.assertEqual(
            self.device._meta.get_field("google_most_recent_user").null, False
        )

    def test_device_model_foreign_key(self):
        self.assertEqual(
            self.device._meta.get_field("device_model").related_model, DeviceModel
        )

    def test_device_model_required(self):
        self.assertEqual(self.device._meta.get_field("device_model").blank, False)
        self.assertEqual(self.device._meta.get_field("device_model").null, False)

    def test_building_foreign_key(self):
        self.assertEqual(
            self.device._meta.get_field("building").related_model, Building
        )

    def test_building_optional(self):
        self.assertEqual(self.device._meta.get_field("building").blank, True)
        self.assertEqual(self.device._meta.get_field("building").null, True)

    def test_room_foreign_key(self):
        self.assertEqual(self.device._meta.get_field("room").related_model, Room)

    def test_room_optional(self):
        self.assertEqual(self.device._meta.get_field("room").blank, True)
        self.assertEqual(self.device._meta.get_field("room").null, True)

    ### Functions ###
    def test___str__(self):
        device = DeviceFactory(
            asset_id="test_asset_id", serial_number="test_serial_number"
        )
        self.assertEqual(
            device.__str__(),
            f"test_asset_id (test_serial_number) - {device.device_model}",
        )

    def test_display_name_with_asset_id(self):
        device = DeviceFactory(
            asset_id="test_asset_id", serial_number="test_serial_number"
        )
        self.assertEqual(
            device.display_name(),
            f"test_asset_id (test_serial_number)",
        )

    def test_display_name_without_asset_id(self):
        device = DeviceFactory(asset_id="", serial_number="test_serial_number")
        self.assertEqual(
            device.display_name(),
            f"test_serial_number",
        )

    def test_get_absolute_url(self):
        self.assertEqual(self.device.get_absolute_url(), "/devices/1/")


class DeviceAccessoryTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        DeviceAccessoryFactory(id=1)

    def setUp(self):
        self.device_accessory = DeviceAccessory.objects.get(id=1)

    def test_name_label(self):
        name_label = self.device_accessory._meta.get_field("name").verbose_name
        self.assertEqual(name_label, "name")

    def test_name_max_length(self):
        max_length = self.device_accessory._meta.get_field("name").max_length
        self.assertEqual(max_length, 255)

    def test_name_unique(self):
        unique = self.device_accessory._meta.get_field("name").unique
        self.assertTrue(unique)

    def test_device_models_foreign_key(self):
        self.assertEqual(
            self.device_accessory._meta.get_field("device_models").related_model,
            DeviceModel,
        )

    ### Functions ###
    def test___str__(self):
        device_manufacturer = DeviceManufacturerFactory(name="Dell")
        device_models = DeviceModelFactory.create_batch(
            2, manufacturer=device_manufacturer
        )
        # device_accessory = DeviceAccessory(name="test", device_models=device_models)
        device_accessory = DeviceAccessoryFactory.create(
            name="test", device_models=device_models
        )
        device_models = device_accessory.device_models.all()
        device_model_names = ",".join([x.name for x in device_models])
        self.assertEqual(
            device_accessory.__str__(),
            f"{device_accessory.name} ({ device_model_names })",
        )
