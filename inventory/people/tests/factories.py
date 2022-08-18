import factory
from faker import Faker
from faker.providers import (
    person as PersonProvider,
    internet as InternetProvider,
    misc as MiscProvider,
)
from factory.django import DjangoModelFactory
from people.models import Person, PersonStatus, PersonType
from locations.tests.factories import BuildingFactory, RoomFactory

# Faker Setup
fake = Faker()
Faker.seed(0)
fake.add_provider(PersonProvider)
fake.add_provider(InternetProvider)
fake.add_provider(MiscProvider)


class PersonStatusFactory(DjangoModelFactory):
    class Meta:
        model = PersonStatus
        django_get_or_create = ("name",)

    name = fake.random_choices(elements=("Active", "Inactive"), length=1)[0]
    is_inactive = False


class PersonTypeFactory(DjangoModelFactory):
    class Meta:
        model = PersonType
        django_get_or_create = ("name",)

    name = fake.random_choices(elements=("Staff", "Student"), length=1)[0]


class PersonFactory(DjangoModelFactory):
    class Meta:
        model = Person

    first_name = fake.first_name()
    middle_name = fake.first_name()
    last_name = fake.last_name()
    email = factory.LazyFunction(lambda: fake.unique.ascii_company_email())
    internal_id = factory.LazyFunction(lambda: fake.unique.numerify("%##!"))
    type = factory.SubFactory(PersonTypeFactory)
    status = factory.SubFactory(PersonStatusFactory)
    primary_building = factory.SubFactory(BuildingFactory)
    primary_room = factory.SubFactory(RoomFactory)

    @factory.post_generation
    def buildings(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        if not extracted:
            extracted = BuildingFactory.create_batch(10)
        self.buildings.add(*extracted)

    @factory.post_generation
    def rooms(self, create, extracted, **kwargs):
        if not create:
            return
        if not extracted:
            extracted = RoomFactory.create_batch(10)
        self.rooms.add(*extracted)


class PersonWithBuildingsFactory(PersonFactory):
    @factory.post_generation
    def buildings(self, create, extracted, **kwargs):
        if not create:
            return
        if not extracted:
            extracted = BuildingFactory.create_batch(10)
        self.buildings.add(*extracted)


class PersonWithRoomsFactory(PersonFactory):
    @factory.post_generation
    def rooms(self, create, extracted, **kwargs):
        if not create:
            return
        if not extracted:
            extracted = RoomFactory.create_batch(10)
        self.rooms.add(*extracted)
