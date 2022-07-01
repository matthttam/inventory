import factory
from faker import Faker
from faker.providers import company as CompanyProvider
from factory.django import DjangoModelFactory
from devices.models import DeviceManufacturer, DeviceStatus, DeviceModel, Device

# Faker Setup
fake = Faker()
Faker.seed(0)
fake.add_provider(CompanyProvider)


class DeviceManufacturerFactory(DjangoModelFactory):
    class Meta:
        model = DeviceManufacturer

    name = fake.company()  # factory.Faker("catch_phrase")


class DeviceStatusFactory(DjangoModelFactory):
    class Meta:
        model = DeviceStatus
        django_get_or_create = ("name",)

    name = fake.random_choices(elements=("Active", "Inactive"))


class DeviceModelFactory(DjangoModelFactory):
    class Meta:
        model = DeviceModel

    name = "test_model"
    manufacturer = factory.SubFactory(DeviceManufacturerFactory)


class DeviceFactory(DjangoModelFactory):
    class Meta:
        model = Device
        django_get_or_create = ("serial_number", "asset_id", "google_id")

    serial_number = factory.Sequence(lambda n: f"SN-{n}")
    asset_id = factory.Sequence(lambda n: f"ASSET-{n}")
    notes = ""
    google_id = None
    status = factory.SubFactory(DeviceStatusFactory)
    device_model = factory.SubFactory(DeviceModelFactory)
    building = None
    room = None
