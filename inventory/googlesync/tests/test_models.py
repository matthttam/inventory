from django.test import TestCase
from unittest.mock import patch
from people.tests.factories import PersonTypeFactory
from people.models import PersonType, Person
from devices.models import Device
from .factories import (
    GoogleConfigFactory,
    GoogleServiceAccountConfigFactory,
    GooglePersonSyncProfileFactory,
    GoogleDeviceSyncProfileFactory,
    GooglePersonMappingFactory,
    GoogleDeviceMappingFactory,
    GooglePersonTranslationFactory,
    GoogleDeviceTranslationFactory,
    GoogleDeviceFactory,
)
from googlesync.models import (
    GoogleConfigAbstract,
    GoogleConfig,
    GoogleServiceAccountConfig,
    GoogleSyncProfileAbstract,
    GooglePersonSyncProfile,
    GoogleDeviceSyncProfile,
    MappingAbstract,
    GooglePersonMapping,
    GoogleDeviceMapping,
    TranslationAbstract,
    GooglePersonTranslation,
    GoogleDeviceTranslation,
    GoogleDevice,
)


class GoogleConfigAbstractTest(TestCase):
    def test_is_abstract(self):
        self.assertTrue(GoogleConfigAbstract._meta.abstract)

    def test_client_id_label(self):
        field_label = GoogleConfigAbstract._meta.get_field("client_id").verbose_name
        self.assertEqual(field_label, "client id")

    def test_client_id_max_length(self):
        max_length = GoogleConfigAbstract._meta.get_field("client_id").max_length
        self.assertEqual(max_length, 255)

    def test_project_id_label(self):
        field_label = GoogleConfigAbstract._meta.get_field("project_id").verbose_name
        self.assertEqual(field_label, "project id")

    def test_project_id_max_length(self):
        max_length = GoogleConfigAbstract._meta.get_field("project_id").max_length
        self.assertEqual(max_length, 255)

    def test_auth_uri_label(self):
        field_label = GoogleConfigAbstract._meta.get_field("auth_uri").verbose_name
        self.assertEqual(field_label, "auth uri")

    def test_auth_uri_max_length(self):
        max_length = GoogleConfigAbstract._meta.get_field("auth_uri").max_length
        self.assertEqual(max_length, 255)

    def test_auth_uri_type_urlfield(self):
        self.assertEqual(
            type(GoogleConfigAbstract._meta.get_field("auth_uri")).__name__,
            "URLField",
        )

    def test_auth_uri_default_value(self):
        default = GoogleConfigAbstract._meta.get_field("auth_uri").default
        self.assertEqual(default, "https://accounts.google.com/o/oauth2/auth")

    def test_token_uri_label(self):
        field_label = GoogleConfigAbstract._meta.get_field("token_uri").verbose_name
        self.assertEqual(field_label, "token uri")

    def test_token_uri_max_length(self):
        max_length = GoogleConfigAbstract._meta.get_field("token_uri").max_length
        self.assertEqual(max_length, 255)

    def test_token_uri_type_urlfield(self):
        self.assertEqual(
            type(GoogleConfigAbstract._meta.get_field("token_uri")).__name__,
            "URLField",
        )

    def test_token_uri_default_value(self):
        default = GoogleConfigAbstract._meta.get_field("token_uri").default
        self.assertEqual(default, "https://oauth2.googleapis.com/token")

    def test_auth_provider_x509_cert_url_label(self):
        field_label = GoogleConfigAbstract._meta.get_field(
            "auth_provider_x509_cert_url"
        ).verbose_name
        self.assertEqual(field_label, "auth provider x509 cert url")

    def test_auth_provider_x509_cert_url_max_length(self):
        max_length = GoogleConfigAbstract._meta.get_field(
            "auth_provider_x509_cert_url"
        ).max_length
        self.assertEqual(max_length, 255)

    def test_auth_provider_x509_cert_url_type_urlfield(self):
        self.assertEqual(
            type(
                GoogleConfigAbstract._meta.get_field("auth_provider_x509_cert_url")
            ).__name__,
            "URLField",
        )

    def test_auth_provider_x509_cert_url_default_value(self):
        GoogleConfigAbstract._meta
        default = GoogleConfigAbstract._meta.get_field(
            "auth_provider_x509_cert_url"
        ).default
        self.assertEqual(default, "https://www.googleapis.com/oauth2/v1/certs")


class GoogleConfigTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        GoogleConfigFactory()

    def setUp(self):
        self.google_config = GoogleConfig.objects.get(id=1)

    def test_subclass(self):
        self.assertTrue(issubclass(GoogleConfig, GoogleConfigAbstract))

    def test_client_secret_label(self):
        field_label = self.google_config._meta.get_field("client_secret").verbose_name
        self.assertEqual(field_label, "client secret")

    def test_client_secret_max_length(self):
        max_length = self.google_config._meta.get_field("client_secret").max_length
        self.assertEqual(max_length, 255)

    ### Functions ###
    def test___str__(self):
        google_config = GoogleConfigFactory(project_id="TEST_PROJECT_ID")
        self.assertEqual(google_config.__str__(), "TEST_PROJECT_ID")

    def test_get_absolute_url(self):
        self.assertEqual(
            self.google_config.get_absolute_url(),
            "/googlesync/config/",
        )


class GoogleServiceAccountConfigTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        GoogleServiceAccountConfigFactory()

    def setUp(self):
        self.google_service_account_config = GoogleServiceAccountConfig.objects.get(
            id=1
        )

    def test_subclass(self):
        self.assertTrue(issubclass(GoogleServiceAccountConfig, GoogleConfigAbstract))

    def test_type_label(self):
        field_label = self.google_service_account_config._meta.get_field(
            "type"
        ).verbose_name
        self.assertEqual(field_label, "type")

    def test_type_max_length(self):
        max_length = self.google_service_account_config._meta.get_field(
            "type"
        ).max_length
        self.assertEqual(max_length, 255)

    def test_type_default_value(self):
        default = self.google_service_account_config._meta.get_field("type").default
        self.assertEqual(default, "service_account")

    def test_private_key_id_label(self):
        field_label = self.google_service_account_config._meta.get_field(
            "private_key_id"
        ).verbose_name
        self.assertEqual(field_label, "private key id")

    def test_private_key_id_max_length(self):
        max_length = self.google_service_account_config._meta.get_field(
            "private_key_id"
        ).max_length
        self.assertEqual(max_length, 255)

    def test_private_key_label(self):
        field_label = self.google_service_account_config._meta.get_field(
            "private_key"
        ).verbose_name
        self.assertEqual(field_label, "private key")

    def test_private_key_max_length(self):
        max_length = self.google_service_account_config._meta.get_field(
            "private_key"
        ).max_length
        self.assertEqual(max_length, 2048)

    def test_client_email_label(self):
        field_label = self.google_service_account_config._meta.get_field(
            "client_email"
        ).verbose_name
        self.assertEqual(field_label, "client email")

    def test_client_email_max_length(self):
        max_length = self.google_service_account_config._meta.get_field(
            "client_email"
        ).max_length
        self.assertEqual(max_length, 255)

    def test_client_x509_cert_url_label(self):
        field_label = self.google_service_account_config._meta.get_field(
            "client_x509_cert_url"
        ).verbose_name
        self.assertEqual(field_label, "client x509 cert url")

    def test_client_x509_cert_url_max_length(self):
        max_length = self.google_service_account_config._meta.get_field(
            "client_x509_cert_url"
        ).max_length
        self.assertEqual(max_length, 255)

    def test_client_x509_cert_url_type_urlfield(self):
        self.assertEqual(
            type(
                self.google_service_account_config._meta.get_field(
                    "auth_provider_x509_cert_url"
                )
            ).__name__,
            "URLField",
        )

    def test_delegate_label(self):
        field_label = self.google_service_account_config._meta.get_field(
            "delegate"
        ).verbose_name
        self.assertEqual(field_label, "delegate")

    def test_delegate_max_length(self):
        max_length = self.google_service_account_config._meta.get_field(
            "delegate"
        ).max_length
        self.assertEqual(max_length, 255)

    def test_delegate_help_text(self):
        help_text = self.google_service_account_config._meta.get_field(
            "delegate"
        ).help_text
        self.assertEqual(
            help_text,
            "User account to impersonate when accessing Google. User must have rights to the resources needed.",
        )

    def test_target_label(self):
        field_label = self.google_service_account_config._meta.get_field(
            "target"
        ).verbose_name
        self.assertEqual(field_label, "target")

    def test_target_max_length(self):
        max_length = self.google_service_account_config._meta.get_field(
            "target"
        ).max_length
        self.assertEqual(max_length, 255)

    def test_target_help_text(self):
        help_text = self.google_service_account_config._meta.get_field(
            "target"
        ).help_text
        self.assertEqual(
            help_text,
            "Google domain name to connect to (e.g. my.site.com)",
        )

    ### Functions ###
    def test___str__(self):
        google_service_account_config = GoogleServiceAccountConfigFactory(
            private_key_id="test_project_id"
        )
        self.assertEqual(
            google_service_account_config.__str__(),
            f"{google_service_account_config.project_id}",
        )

    def test_get_absolute_url(self):
        self.assertEqual(
            self.google_service_account_config.get_absolute_url(),
            "/googlesync/serviceaccount/",
        )


class GoogleSyncProfileAbstractTest(TestCase):
    def test_is_abstract(self):
        self.assertTrue(GoogleConfigAbstract._meta.abstract)

    def test_name_label(self):
        field_label = GoogleSyncProfileAbstract._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")

    def test_name_max_length(self):
        max_length = GoogleSyncProfileAbstract._meta.get_field("name").max_length
        self.assertEqual(max_length, 255)

    def test_google_service_account_config_foreign_key(self):
        self.assertEqual(
            GoogleSyncProfileAbstract._meta.get_field(
                "google_service_account_config"
            ).related_model,
            GoogleServiceAccountConfig,
        )


class GooglePersonSyncProfileTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        GooglePersonSyncProfileFactory()

    def setUp(self):
        self.google_person_sync_profile = GooglePersonSyncProfile.objects.get(id=1)

    def test_subclass(self):
        self.assertTrue(issubclass(GooglePersonSyncProfile, GoogleSyncProfileAbstract))

    def test_person_type_foreign_key(self):
        self.assertEqual(
            self.google_person_sync_profile._meta.get_field(
                "person_type"
            ).related_model,
            PersonType,
        )

    def test_google_query_label(self):
        field_label = self.google_person_sync_profile._meta.get_field(
            "google_query"
        ).verbose_name
        self.assertEqual(field_label, "google query")

    def test_google_query_max_length(self):
        max_length = self.google_person_sync_profile._meta.get_field(
            "google_query"
        ).max_length
        self.assertEqual(max_length, 1024)

    def test_google_query_optional(self):
        self.assertEqual(
            self.google_person_sync_profile._meta.get_field("google_query").blank, True
        )
        self.assertEqual(
            self.google_person_sync_profile._meta.get_field("google_query").null,
            False,
        )

    def test_google_query_default_value(self):
        default = self.google_person_sync_profile._meta.get_field(
            "google_query"
        ).default
        self.assertEqual(default, "orgUnitPath=/")

    def test_google_query_help_text(self):
        help_text = self.google_person_sync_profile._meta.get_field(
            "google_query"
        ).help_text
        self.assertEqual(
            help_text,
            "Google API query to use when searching for users to sync for this profile. (e.g. 'orgUnitPath=/Staff'). Query documentation: https://developers.google.com/admin-sdk/directory/v1/guides/search-users",
        )

    def test_mappings_related_name(self):
        self.assertEqual(
            self.google_person_sync_profile._meta.get_field("mappings").related_name,
            "mappings",
        )

    ### Functions ###
    def test___str__(self):
        person_type = PersonTypeFactory()
        google_service_account_config = GoogleServiceAccountConfigFactory()
        google_person_sync_profile = GooglePersonSyncProfileFactory(
            name="test_profile_name", person_type=person_type
        )
        self.assertEqual(
            google_person_sync_profile.__str__(),
            f"test_profile_name ({person_type.__str__()}: {google_service_account_config.__str__()})",
        )


class GoogleDeviceSyncProfileTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        GoogleDeviceSyncProfileFactory()

    def setUp(self):
        self.google_device_sync_profile = GoogleDeviceSyncProfile.objects.get(id=1)

    def test_subclass(self):
        self.assertTrue(issubclass(GoogleDeviceSyncProfile, GoogleSyncProfileAbstract))

    def test_google_org_unit_path_label(self):
        field_label = self.google_device_sync_profile._meta.get_field(
            "google_org_unit_path"
        ).verbose_name
        self.assertEqual(field_label, "google org unit path")

    def test_google_org_unit_path_max_length(self):
        max_length = self.google_device_sync_profile._meta.get_field(
            "google_org_unit_path"
        ).max_length
        self.assertEqual(max_length, 1024)

    def test_google_org_unit_path_optional(self):
        self.assertEqual(
            self.google_device_sync_profile._meta.get_field(
                "google_org_unit_path"
            ).blank,
            True,
        )
        self.assertEqual(
            self.google_device_sync_profile._meta.get_field(
                "google_org_unit_path"
            ).null,
            False,
        )

    def test_google_org_unit_path_default_value(self):
        default = self.google_device_sync_profile._meta.get_field(
            "google_org_unit_path"
        ).default
        self.assertEqual(default, "")

    def test_google_org_unit_path_help_text(self):
        help_text = self.google_device_sync_profile._meta.get_field(
            "google_org_unit_path"
        ).help_text
        self.assertEqual(
            help_text,
            "The full path of the organizational unit (minus the leading /) or its unique ID.",
        )

    def test_google_query_label(self):
        field_label = self.google_device_sync_profile._meta.get_field(
            "google_query"
        ).verbose_name
        self.assertEqual(field_label, "google query")

    def test_google_query_max_length(self):
        max_length = self.google_device_sync_profile._meta.get_field(
            "google_query"
        ).max_length
        self.assertEqual(max_length, 1024)

    def test_google_query_optional(self):
        self.assertEqual(
            self.google_device_sync_profile._meta.get_field("google_query").blank, True
        )
        self.assertEqual(
            self.google_device_sync_profile._meta.get_field("google_query").null,
            False,
        )

    def test_google_query_default_value(self):
        default = self.google_device_sync_profile._meta.get_field(
            "google_query"
        ).default
        self.assertEqual(default, "")

    def test_google_query_help_text(self):
        help_text = self.google_device_sync_profile._meta.get_field(
            "google_query"
        ).help_text
        self.assertEqual(
            help_text,
            "Google API query to use when searching for devices to sync for this profile. (e.g. 'location:seattle'). Query documentation: https://developers.google.com/admin-sdk/directory/v1/list-query-operators",
        )

    def test_mappings_related_name(self):
        self.assertEqual(
            self.google_device_sync_profile._meta.get_field("mappings").related_name,
            "mappings",
        )

    ### Functions ###
    def test___str__(self):
        GooglePersonSyncProfileFactory()
        person_type = PersonTypeFactory()
        google_service_account_config = GoogleServiceAccountConfigFactory()
        google_person_sync_profile = GooglePersonSyncProfileFactory(
            name="test_profile_name", person_type=person_type
        )
        self.assertEqual(
            google_person_sync_profile.__str__(),
            f"test_profile_name ({person_type.__str__()}: {google_service_account_config.__str__()})",
        )


class MappingAbstractTest(TestCase):
    def test_is_abstract(self):
        self.assertTrue(MappingAbstract._meta.abstract)

    def test_from_field_label(self):
        field_label = MappingAbstract._meta.get_field("from_field").verbose_name
        self.assertEqual(field_label, "from field")

    def test_from_field_max_length(self):
        max_length = MappingAbstract._meta.get_field("from_field").max_length
        self.assertEqual(max_length, 255)

    def test_to_field_label(self):
        field_label = MappingAbstract._meta.get_field("to_field").verbose_name
        self.assertEqual(field_label, "to field")

    def test_to_field_max_length(self):
        max_length = MappingAbstract._meta.get_field("to_field").max_length
        self.assertEqual(max_length, 255)

    def test_matching_priority_label(self):
        field_label = MappingAbstract._meta.get_field("matching_priority").verbose_name
        self.assertEqual(field_label, "matching priority")

    def test_matching_priority_choices(self):
        choices = MappingAbstract._meta.get_field("matching_priority").choices
        potential_choices = [(x, x) for x in range(1, 10)]
        self.assertCountEqual(potential_choices, choices)

    def test_matching_priority_unique(self):
        unique = MappingAbstract._meta.get_field("matching_priority").unique
        self.assertTrue(unique)

    def test_matching_priority_optional(self):
        self.assertEqual(
            MappingAbstract._meta.get_field("matching_priority").blank, True
        )
        self.assertEqual(
            MappingAbstract._meta.get_field("matching_priority").null, True
        )

    ### Functions ###
    @patch("googlesync.models.MappingAbstract._meta.abstract", set())
    def test___str__(self):
        google_person_mapping = MappingAbstract(
            from_field="from field", to_field="to field"
        )
        self.assertEqual(
            google_person_mapping.__str__(),
            "from field => to field",
        )


class GooglePersonMappingTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        GooglePersonMappingFactory()

    def setUp(self):
        self.google_person_mapping = GooglePersonMapping.objects.get(id=1)

    def test_subclass(self):
        self.assertTrue(issubclass(GooglePersonMapping, MappingAbstract))

    def test_sync_profile_foreign_key(self):
        self.assertEqual(
            self.google_person_mapping._meta.get_field("sync_profile").related_model,
            GooglePersonSyncProfile,
        )

    def test_translations_related_name(self):
        self.assertEqual(
            self.google_person_mapping._meta.get_field("translations").related_name,
            "translations",
        )

    def test_to_field_label(self):
        field_label = self.google_person_mapping._meta.get_field(
            "to_field"
        ).verbose_name
        self.assertEqual(field_label, "to field")

    def test_to_field_max_length(self):
        max_length = self.google_person_mapping._meta.get_field("to_field").max_length
        self.assertEqual(max_length, 255)

    def test_to_field_choices_not_contain_id(self):
        choices = self.google_person_mapping._meta.get_field("to_field").choices
        self.assertNotIn("id", choices)

    def test_to_field_choices(self):
        choices = self.google_person_mapping._meta.get_field("to_field").choices
        potential_choices = [
            (f.name, f.verbose_name) for f in Person._meta.fields if f.name != "id"
        ]
        self.assertCountEqual(potential_choices, choices)

    ### Functions ###
    def test_get_absolute_url(self):
        self.assertEqual(
            self.google_person_mapping.get_absolute_url(),
            "/googlesync/personmapping/1/edit/",
        )


class GoogleDeviceMappingTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        GoogleDeviceMappingFactory()

    def setUp(self):
        self.google_device_mapping = GoogleDeviceMapping.objects.get(id=1)

    def test_subclass(self):
        self.assertTrue(issubclass(GoogleDeviceMapping, MappingAbstract))

    def test_sync_profile_foreign_key(self):
        self.assertEqual(
            self.google_device_mapping._meta.get_field("sync_profile").related_model,
            GoogleDeviceSyncProfile,
        )

    def test_translations_related_name(self):
        self.assertEqual(
            self.google_device_mapping._meta.get_field("translations").related_name,
            "translations",
        )

    def test_to_field_label(self):
        field_label = self.google_device_mapping._meta.get_field(
            "to_field"
        ).verbose_name
        self.assertEqual(field_label, "to field")

    def test_to_field_max_length(self):
        max_length = self.google_device_mapping._meta.get_field("to_field").max_length
        self.assertEqual(max_length, 255)

    def test_to_field_choices_not_contain_id(self):
        choices = self.google_device_mapping._meta.get_field("to_field").choices
        self.assertIn(("id", "id"), choices)

    def test_to_field_choices(self):
        choices = self.google_device_mapping._meta.get_field("to_field").choices
        potential_choices = [
            (f.name, f.verbose_name) for f in GoogleDevice._meta.fields
        ]
        self.assertCountEqual(potential_choices, choices)

    ### Functions ###
    def test_get_absolute_url(self):
        self.assertEqual(
            self.google_device_mapping.get_absolute_url(),
            "/googlesync/devicemapping/1/edit/",
        )


class TranslationAbstractTest(TestCase):
    def test_is_abstract(self):
        self.assertTrue(TranslationAbstract._meta.abstract)

    def test_translate_from_label(self):
        field_label = TranslationAbstract._meta.get_field("translate_from").verbose_name
        self.assertEqual(field_label, "translate from")

    def test_translate_from_max_length(self):
        max_length = TranslationAbstract._meta.get_field("translate_from").max_length
        self.assertEqual(max_length, 255)

    def test_translate_to_label(self):
        field_label = TranslationAbstract._meta.get_field("translate_to").verbose_name
        self.assertEqual(field_label, "translate to")

    def test_translate_to_max_length(self):
        max_length = TranslationAbstract._meta.get_field("translate_to").max_length
        self.assertEqual(max_length, 255)


class GooglePersonTranslationTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        GooglePersonTranslationFactory()

    def setUp(self):
        self.google_person_translation = GooglePersonTranslation.objects.get(id=1)

    def test_subclass(self):
        self.assertTrue(issubclass(GooglePersonTranslation, TranslationAbstract))

    def test_google_person_mapping_foreign_key(self):
        self.assertEqual(
            self.google_person_translation._meta.get_field(
                "google_person_mapping"
            ).related_model,
            GooglePersonMapping,
        )

    ### Functions ###
    def test___str__(self):
        google_person_mapping = GooglePersonMappingFactory(to_field="person field")
        google_person_translation = GooglePersonTranslationFactory(
            google_person_mapping=google_person_mapping,
            translate_from="translate from",
            translate_to="translate to",
        )
        self.assertEqual(
            google_person_translation.__str__(),
            "Translate 'person field' from 'translate from' to 'translate to'",
        )


class GoogleDeviceTranslationTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        GoogleDeviceTranslationFactory()

    def setUp(self):
        self.google_device_translation = GoogleDeviceTranslation.objects.get(id=1)

    def test_subclass(self):
        self.assertTrue(issubclass(GoogleDeviceTranslation, TranslationAbstract))

    def test_google_device_mapping_foreign_key(self):
        self.assertEqual(
            self.google_device_translation._meta.get_field(
                "google_device_mapping"
            ).related_model,
            GoogleDeviceMapping,
        )

    ### Functions ###
    def test___str__(self):
        google_device_mapping = GoogleDeviceMappingFactory(to_field="device field")
        google_device_translation = GoogleDeviceTranslationFactory(
            google_device_mapping=google_device_mapping,
            translate_from="translate from",
            translate_to="translate to",
        )
        self.assertEqual(
            google_device_translation.__str__(),
            "Translate 'device field' from 'translate from' to 'translate to'",
        )


class GoogleDeviceTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.google_device_id = GoogleDeviceFactory().id

    def setUp(self):
        self.google_device = GoogleDevice.objects.get(id=self.google_device_id)

    def test_id_label(self):
        field_label = self.google_device._meta.get_field("id").verbose_name
        self.assertEqual(field_label, "id")

    def test_id_max_length(self):
        max_length = self.google_device._meta.get_field("id").max_length
        self.assertEqual(max_length, 255)

    def test_id_unique(self):
        unique = self.google_device._meta.get_field("id").unique
        self.assertTrue(unique)

    def test_id_required(self):
        self.assertEqual(self.google_device._meta.get_field("id").blank, False)
        self.assertEqual(self.google_device._meta.get_field("id").null, False)

    def test_status_label(self):
        field_label = self.google_device._meta.get_field("status").verbose_name
        self.assertEqual(field_label, "status")

    def test_status_max_length(self):
        max_length = self.google_device._meta.get_field("status").max_length
        self.assertEqual(max_length, 255)

    def test_status_optional(self):
        self.assertEqual(self.google_device._meta.get_field("status").blank, True)
        self.assertEqual(self.google_device._meta.get_field("status").null, True)

    def test_organization_unit_label(self):
        field_label = self.google_device._meta.get_field(
            "organization_unit"
        ).verbose_name
        self.assertEqual(field_label, "organization unit")

    def test_organization_unit_max_length(self):
        max_length = self.google_device._meta.get_field("organization_unit").max_length
        self.assertEqual(max_length, 255)

    def test_organization_unit_optional(self):
        self.assertEqual(
            self.google_device._meta.get_field("organization_unit").blank, True
        )
        self.assertEqual(
            self.google_device._meta.get_field("organization_unit").null, True
        )

    def test_enrollment_time_label(self):
        field_label = self.google_device._meta.get_field("enrollment_time").verbose_name
        self.assertEqual(field_label, "enrollment time")

    def test_enrollment_time_optional(self):
        self.assertEqual(
            self.google_device._meta.get_field("enrollment_time").blank, True
        )
        self.assertEqual(
            self.google_device._meta.get_field("enrollment_time").null, True
        )

    def test_last_policy_sync_label(self):
        field_label = self.google_device._meta.get_field(
            "last_policy_sync"
        ).verbose_name
        self.assertEqual(field_label, "last policy sync")

    def test_last_policy_sync_optional(self):
        self.assertEqual(
            self.google_device._meta.get_field("last_policy_sync").blank, True
        )
        self.assertEqual(
            self.google_device._meta.get_field("last_policy_sync").null, True
        )

    def test_location_label(self):
        field_label = self.google_device._meta.get_field("location").verbose_name
        self.assertEqual(field_label, "location")

    def test_location_max_length(self):
        max_length = self.google_device._meta.get_field("location").max_length
        self.assertEqual(max_length, 255)

    def test_location_optional(self):
        self.assertEqual(self.google_device._meta.get_field("location").blank, True)
        self.assertEqual(self.google_device._meta.get_field("location").null, True)

    def test_most_recent_user_label(self):
        field_label = self.google_device._meta.get_field(
            "most_recent_user"
        ).verbose_name
        self.assertEqual(field_label, "most recent user")

    def test_most_recent_user_max_length(self):
        max_length = self.google_device._meta.get_field("most_recent_user").max_length
        self.assertEqual(max_length, 255)

    def test_most_recent_user_optional(self):
        self.assertEqual(
            self.google_device._meta.get_field("most_recent_user").blank, True
        )
        self.assertEqual(
            self.google_device._meta.get_field("most_recent_user").null, True
        )
