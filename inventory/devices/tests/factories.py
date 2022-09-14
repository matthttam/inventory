import factory
from faker import Faker
from faker.providers import company as CompanyProvider, lorem as LoremProvider

from factory.django import DjangoModelFactory
from googlesync.tests.factories import GoogleDeviceFactory
from devices.models import (
    DeviceManufacturer,
    DeviceStatus,
    DeviceModel,
    Device,
    DeviceAccessory,
    DeviceTag,
)
from django.core.files.base import ContentFile

# Faker Setup
fake = Faker()
Faker.seed(0)
fake.add_provider(CompanyProvider)


def get_device_tag_generator(filename="example.jpg", width=300, height=300):
    return lambda _: ContentFile(
        factory.django.ImageField()._make_data({"width": width, "height": height}),
        filename,
    )


class DeviceTagFactory(DjangoModelFactory):
    class Meta:
        model = DeviceTag
        django_get_or_create = ("name",)

    name = factory.LazyFunction(lambda: fake.unique.company())
    active = True
    factory.LazyFunction(get_device_tag_generator())


class DeviceStatusFactory(DjangoModelFactory):
    class Meta:
        model = DeviceStatus
        django_get_or_create = ("name",)

    name = fake.random_choices(elements=("Active", "Inactive"))
    is_inactive = False


class DeviceManufacturerFactory(DjangoModelFactory):
    class Meta:
        model = DeviceManufacturer

    name = factory.LazyFunction(lambda: fake.unique.company())


class DeviceModelFactory(DjangoModelFactory):
    class Meta:
        model = DeviceModel

    name = factory.Sequence(lambda n: f"DeviceModel-{n}")
    manufacturer = factory.SubFactory(DeviceManufacturerFactory)


class DeviceFactory(DjangoModelFactory):
    class Meta:
        model = Device
        django_get_or_create = ("serial_number", "asset_id")

    google_device = factory.SubFactory(GoogleDeviceFactory)
    serial_number = factory.Sequence(lambda n: f"SN-{n}")
    asset_id = factory.Sequence(lambda n: f"ASSET-{n}")
    notes = ""
    status = factory.SubFactory(DeviceStatusFactory)
    device_model = factory.SubFactory(DeviceModelFactory)
    building = None
    room = None

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        if not extracted:
            extracted = DeviceTagFactory.create_batch(10)
        self.buildings.add(*extracted)


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
