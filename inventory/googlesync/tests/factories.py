import factory
from faker import Faker
from faker.providers import (
    internet as InternetProvider,
    date_time as DateTimeProvider,
    misc as MiscProvider,
)
from factory.django import DjangoModelFactory
from zoneinfo import ZoneInfo
from django.utils import timezone
from googlesync.models import (
    GoogleConfig,
    GoogleCustomSchema,
    GoogleCustomSchemaField,
    GoogleDefaultSchema,
    GoogleDefaultSchemaProperty,
    GoogleDeviceLinkMapping,
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
fake.add_provider(MiscProvider)

tz = ZoneInfo(timezone.settings.TIME_ZONE)


class GoogleConfigFactory(DjangoModelFactory):
    class Meta:
        model = GoogleConfig

    client_id = fake.lexify(text="?" * 30)
    project_id = fake.lexify(text="?" * 30)
    client_secret = fake.lexify(text="?" * 30)


class GoogleServiceAccountConfigFactory(DjangoModelFactory):
    class Meta:
        model = GoogleServiceAccountConfig

    project_id = fake.lexify(text="?" * 30)
    private_key_id = fake.lexify(text="?" * 30)
    private_key = fake.lexify(text="?" * 2000)
    client_email = fake.ascii_safe_email()
    client_id = fake.lexify(text="?" * 30)
    client_x509_cert_url = fake.lexify(text="?" * 30)
    delegate = fake.ascii_safe_email()
    target = fake.url()


class GoogleCustomSchemaFactory(DjangoModelFactory):
    class Meta:
        model = GoogleCustomSchema

    service_account_config = factory.SubFactory(GoogleServiceAccountConfigFactory)
    schema_id = fake.lexify(text="?" * 30)
    schema_name = fake.lexify(text="?" * 30)
    display_name = fake.lexify(text="?" * 30)
    kind = "admin#directory#schema"
    etag = fake.lexify(text="?" * 80)


class GoogleCustomSchemaFieldFactory(DjangoModelFactory):
    class Meta:
        model = GoogleCustomSchemaField

    schema = factory.SubFactory(GoogleCustomSchemaFactory)
    field_name = fake.lexify(text="?" * 30)
    field_id = fake.lexify(text="?" * 30)
    field_type = "STRING"
    multi_valued = fake.boolean()
    kind = fake.lexify(text="?" * 30)
    etag = fake.lexify(text="?" * 30)
    indexed = fake.boolean()
    display_name = fake.lexify(text="?" * 30)
    read_access_type = fake.lexify(text="?" * 30)
    numeric_indexing_spec_min_value = None
    numeric_indexing_spec_max_value = None


class GoogleDefaultSchemaFactory(DjangoModelFactory):
    class Meta:
        model = GoogleDefaultSchema

    service_account_config = factory.SubFactory(GoogleServiceAccountConfigFactory)
    description = fake.lexify(text="?" * 200)
    schema_id = "User"
    type = "object"


class GoogleDefaultSchemaPropertyFactory(DjangoModelFactory):
    class Meta:
        model = GoogleDefaultSchemaProperty

    schema = factory.SubFactory(GoogleDefaultSchemaFactory)
    parent = None
    etag = fake.lexify(text="?" * 30)
    format = fake.lexify(text="?" * 30)
    type = "string"
    description = fake.lexify(text="?" * 200)


class GooglePersonSyncProfileFactory(DjangoModelFactory):
    class Meta:
        model = GooglePersonSyncProfile

    name = fake.lexify(text="?" * 30)
    person_type = factory.SubFactory(PersonTypeFactory)
    google_service_account_config = factory.SubFactory(
        GoogleServiceAccountConfigFactory
    )
    domain = fake.ascii_safe_email().split("@")[1]


class GooglePersonMappingFactory(DjangoModelFactory):
    class Meta:
        model = GooglePersonMapping

    sync_profile = factory.SubFactory(GooglePersonSyncProfileFactory)
    from_field = factory.SubFactory(GoogleDefaultSchemaPropertyFactory)
    to_field = fake.random_elements(
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


class GoogleDeviceMappingFactory(DjangoModelFactory):
    class Meta:
        model = GoogleDeviceMapping

    sync_profile = factory.SubFactory(GoogleDeviceSyncProfileFactory)
    from_field = factory.SubFactory(GoogleDefaultSchemaPropertyFactory)
    to_field = fake.random_elements(
        elements=[f.name for f in Device._meta.fields if f.name != "id"],
    )[0]


class GoogleDeviceLinkMappingFactory(DjangoModelFactory):
    class Meta:
        model = GoogleDeviceLinkMapping

    sync_profile = factory.SubFactory(GoogleDeviceSyncProfileFactory)
    from_field = fake.random_elements(
        elements=[f.name for f in GoogleDevice._meta.fields if f.name != "id"],
    )[0]
    to_field = fake.random_elements(
        elements=[f.name for f in Device._meta.fields if f.name != "id"],
    )[0]


class GoogleDeviceTranslationFactory(DjangoModelFactory):
    class Meta:
        model = GoogleDeviceTranslation

    google_device_mapping = factory.SubFactory(GoogleDeviceMappingFactory)
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
