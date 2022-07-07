import factory
from faker import Faker
from faker.providers import internet as InternetProvider, date_time as DateTimeProvider
from factory.django import DjangoModelFactory
from zoneinfo import ZoneInfo
from django.utils import timezone
from googlesync.models import (
    GoogleConfig,
    GoogleServiceAccountConfig,
    GooglePersonSyncProfile,
    GooglePersonMapping,
    GooglePersonTranslation,
    GoogleDeviceSyncProfile,
    GoogleDeviceMapping,
    GoogleDeviceTranslation,
    GoogleDevice,
)

from people.tests.factories import PersonTypeFactory
from people.models import Person
from devices.models import Device

# Faker Setup
fake = Faker()
Faker.seed(0)
fake.add_provider(InternetProvider)
fake.add_provider(DateTimeProvider)

tz = ZoneInfo(timezone.settings.TIME_ZONE)


class GoogleConfigFactory(DjangoModelFactory):
    class Meta:
        model = GoogleConfig

    client_id = fake.lexify(text="?" * 30)
    project_id = fake.lexify(text="?" * 30)
    auth_uri = None
    token_uri = None
    auth_provider_x09_cert_url = None
    client_secret = fake.lexify(text="?" * 30)


class GoogleServiceAccountConfigFactory(DjangoModelFactory):
    class Meta:
        model = GoogleServiceAccountConfig

    type = None
    project_id = fake.lexify(text="?" * 30)
    private_key_id = fake.lexify(text="?" * 30)
    private_key = fake.lexify(text="?" * 2000)
    client_email = fake.ascii_safe_email()
    client_id = fake.lexify(text="?" * 30)
    auth_uri = None
    token_uri = None
    auth_provider_x09_cert_url = None
    client_x509_cert_url = fake.lexify(text="?" * 30)
    delegate = fake.ascii_safe_email()
    target = fake.url()


class GooglePersonSyncProfileFactory(DjangoModelFactory):
    class Meta:
        model = GooglePersonSyncProfile

    name = fake.lexify(text="?" * 30)
    person_type = factory.SubFactory(PersonTypeFactory)
    google_service_account_config = factory.SubFactory(
        GoogleServiceAccountConfigFactory
    )
    google_query = None


class GooglePersonMappingFactory(DjangoModelFactory):
    class Meta:
        model = GooglePersonMapping

    google_person_sync_profile = factory.SubFactory(GooglePersonSyncProfileFactory)
    google_field = fake.lexify(text="?" * 30)
    person_field = fake.random_elements(
        elements=[f.name for f in Person._meta.fields if f.name != "id"],
        length=1,
    )[0]
    matching_priority = None


class GooglePersonTranslationFactory(DjangoModelFactory):
    class Meta:
        model = GooglePersonTranslation

    google_person_mapping = factory.SubFactory(GooglePersonMappingFactory)
    translate_from = fake.lexify(text="?" * 10)
    translate_to = fake.lexify(text="?" * 10)


class GoogleDeviceSyncProfileFactory(DjangoModelFactory):
    class Meta:
        model = GoogleDeviceSyncProfile

    name = fake.lexify(text="?" * 30)
    google_service_account_config = factory.SubFactory(
        GoogleServiceAccountConfigFactory
    )
    google_org_unit_path = fake.lexify(text="?" * 50)
    google_query = None


class GoogleDeviceMappingFactory(DjangoModelFactory):
    class Meta:
        model = GoogleDeviceMapping

    google_device_sync_profile = factory.SubFactory(GoogleDeviceSyncProfileFactory)
    google_field = fake.lexify(text="?" * 30)
    device_field = fake.random_elements(
        elements=[f.name for f in Device._meta.fields if f.name != "id"],
    )[0]
    matching_priority = None


class GoogleDeviceTranslationFactory(DjangoModelFactory):
    class Meta:
        model = GoogleDeviceTranslation

    translate_from = fake.lexify(text="?" * 30)
    translate_to = fake.lexify(text="?" * 30)


class GoogleDeviceFactory(DjangoModelFactory):
    class Meta:
        model = GoogleDevice

    id = factory.LazyFunction(lambda: fake.unique.numerify(text="%###################"))
    serial_number = factory.Sequence(lambda n: f"SN-{n}")
    device_model = fake.lexify(text="?" * 30)
    status = fake.lexify(text="?" * 30)
    organization_unit = fake.lexify(text="?" * 30)
    enrollment_time = fake.date_time_this_decade(before_now=True, tzinfo=tz)
    last_policy_sync = factory.LazyAttribute(
        lambda o: fake.date_time_between_dates(
            datetime_start=o.enrollment_time, datetime_end=timezone.now(), tzinfo=tz
        )
    )
    location = fake.lexify(text="?" * 30)
    most_recent_user = fake.lexify(text="?" * 30)
    annotated_asset_id = fake.lexify(text="?" * 30)
