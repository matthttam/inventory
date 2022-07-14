import factory
from faker import Faker
from faker.providers import company as CompanyProvider, lorem as LoremProvider

from factory.django import DjangoModelFactory

from devices.models import (
    DeviceManufacturer,
    DeviceStatus,
    DeviceModel,
    Device,
    DeviceAccessory,
)

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
    is_inactive = False


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


class DeviceAccessoryFactory(DjangoModelFactory):
    class Meta:
        model = DeviceAccessory

    name = factory.LazyFunction(lambda: fake.unique.text(max_nb_chars=10))

    @factory.post_generation
    def device_models(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.device_models.add(*extracted)


class DeviceAccessoryWithDeviceModelsFactory(DeviceAccessoryFactory):
    @factory.post_generation
    def device_models(self, create, extracted, **kwargs):
        if not create:
            return
        if not extracted:
            extracted = DeviceModelFactory.create_batch(fake.random_int(min=1, max=3))
        self.device_models.add(*extracted)
