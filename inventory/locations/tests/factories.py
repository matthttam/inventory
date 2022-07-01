import factory
import re
from faker import Faker
from faker.providers import misc as MiscProvider
from faker_education import SchoolProvider
from factory.django import DjangoModelFactory
from locations.models import Room, Building

# Faker Setup
fake = Faker()
Faker.seed(0)
fake.add_provider(SchoolProvider)
fake.add_provider(MiscProvider)


class BuildingFactory(DjangoModelFactory):
    class Meta:
        model = Building

    # def __init__(self, *args, **kwargs):
    #    super(*args, **kwargs)

    name = fake.unique.school_name()  # factory.faker("")
    internal_id = fake.unique.school_nces_id()
    acronym = factory.LazyAttribute(
        lambda o: "".join(re.findall("(?<![a-z])[A-Z]", o.name))
    )
    active = fake.boolean(chance_of_getting_true=95)


class RoomFactory(DjangoModelFactory):
    class Meta:
        model = Room

    number = "-".join(
        filter(
            None,
            [
                fake.unique.numerify("%#!"),
                fake.random_choices([fake.lexify("?", letters="ABC"), ""], length=1)[0],
            ],
        )
    )
    building = factory.SubFactory(BuildingFactory)
    active = fake.boolean(chance_of_getting_true=95)
