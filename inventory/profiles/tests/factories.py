import factory
from factory.django import DjangoModelFactory
from profiles.models import Profile
from authentication.tests.factories import UserFactory


class ProfileFactory(DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory)
