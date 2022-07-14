import factory
from faker import Faker
from faker.providers import (
    person as PersonProvider,
    misc as MiscProvider,
    internet as InternetProvider,
)
from factory.django import DjangoModelFactory
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

# Faker Setup
fake = Faker()
Faker.seed(0)
fake.add_provider(PersonProvider)
fake.add_provider(MiscProvider)
fake.add_provider(InternetProvider)


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    first_name = fake.first_name()
    last_name = fake.last_name()
    username = factory.LazyFunction(lambda: fake.unique.ascii_company_email())
    password = factory.PostGenerationMethodCall(
        "set_password", fake.password(length=20)
    )
    email = factory.SelfAttribute("username")
    is_active = True
    is_staff = False


class StaffUserFactory(UserFactory):
    is_staff = True
