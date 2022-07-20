import factory
from faker import Faker
from zoneinfo import ZoneInfo
from django.utils import timezone
from factory.django import DjangoModelFactory
from assignments.models import DeviceAssignment, DeviceAccessoryAssignment
from devices.tests.factories import DeviceFactory
from people.tests.factories import PersonFactory
from devices.tests.factories import DeviceFactory, DeviceAccessoryFactory

# Faker Setup
fake = Faker()
Faker.seed(0)

tz = ZoneInfo(timezone.settings.TIME_ZONE)


class DeviceAssignmentFactory(DjangoModelFactory):
    class Meta:
        model = DeviceAssignment

    assignment_datetime = fake.date_time_this_year(before_now=True, tzinfo=tz)
    return_datetime = None
    person = factory.SubFactory(PersonFactory)
    device = factory.SubFactory(DeviceFactory)


class DeviceAccessoryAssignmentFactory(DjangoModelFactory):
    class Meta:
        model = DeviceAccessoryAssignment

    assignment_datetime = fake.date_time_this_year(before_now=True, tzinfo=tz)
    return_datetime = None
    person = factory.SubFactory(PersonFactory)
    device_accessory = factory.SubFactory(DeviceAccessoryFactory)
