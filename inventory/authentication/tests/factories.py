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
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

# Faker Setup
fake = Faker()
Faker.seed(0)
fake.add_provider(PersonProvider)
fake.add_provider(MiscProvider)
fake.add_provider(InternetProvider)


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = (
            "email",
            "username",
        )

    first_name = fake.first_name()
    last_name = fake.last_name()
    username = factory.LazyFunction(lambda: fake.unique.ascii_company_email())
    password = factory.PostGenerationMethodCall(
        "set_password", fake.password(length=20)
    )
    email = factory.SelfAttribute("username")
    is_active = True
    is_staff = False
    is_superuser = False

    @factory.post_generation
    def user_permissions(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for model, permission in extracted:
                content_type = ContentType.objects.get_for_model(model)
                self.user_permissions.add(
                    Permission.objects.get_or_create(
                        codename=permission, content_type=content_type
                    )[0]
                )
            # Expect a list of tuples (ModelClass, "my_permission")


class SuperuserUserFactory(UserFactory):
    is_superuser = True


class StaffUserFactory(UserFactory):
    is_staff = True
