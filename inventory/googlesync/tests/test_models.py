from datetime import datetime
from typing import Any
from unittest import mock
from django.test import TestCase
from django.db.models import UniqueConstraint
from django.db import models

from unittest.mock import MagicMock, PropertyMock, patch

from people.tests.factories import PersonTypeFactory
from people.models import PersonType, Person
from devices.models import Device
from .factories import (
    GoogleConfigFactory,
    GoogleCustomSchemaFactory,
    GoogleDefaultSchemaFactory,
    GoogleDefaultSchemaPropertyFactory,
    GoogleDeviceLinkMappingFactory,
    GoogleServiceAccountConfigFactory,
    GooglePersonSyncProfileFactory,
    GoogleDeviceSyncProfileFactory,
    GooglePersonMappingFactory,
    GoogleDeviceMappingFactory,
    GooglePersonTranslationFactory,
    GoogleDeviceTranslationFactory,
    GoogleDeviceFactory,
    GoogleCustomSchemaFieldFactory,
)
from googlesync.models import (
    GoogleConfigAbstract,
    GoogleConfig,
    GoogleCustomSchema,
    GoogleCustomSchemaField,
    GoogleDefaultSchema,
    GoogleDefaultSchemaProperty,
    GoogleDeviceLinkMapping,
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
        self.google_schema = GoogleServiceAccountConfig.objects.get(id=1)

    def test_subclass(self):
        self.assertTrue(issubclass(GoogleServiceAccountConfig, GoogleConfigAbstract))

    def test_type_label(self):
        field_label = self.google_schema._meta.get_field("type").verbose_name
        self.assertEqual(field_label, "type")

    def test_type_max_length(self):
        max_length = self.google_schema._meta.get_field("type").max_length
        self.assertEqual(max_length, 255)

    def test_type_default_value(self):
        default = self.google_schema._meta.get_field("type").default
        self.assertEqual(default, "service_account")

    def test_private_key_id_label(self):
        field_label = self.google_schema._meta.get_field("private_key_id").verbose_name
        self.assertEqual(field_label, "private key id")

    def test_private_key_id_max_length(self):
        max_length = self.google_schema._meta.get_field("private_key_id").max_length
        self.assertEqual(max_length, 255)

    def test_private_key_label(self):
        field_label = self.google_schema._meta.get_field("private_key").verbose_name
        self.assertEqual(field_label, "private key")

    def test_private_key_max_length(self):
        max_length = self.google_schema._meta.get_field("private_key").max_length
        self.assertEqual(max_length, 2048)

    def test_client_email_label(self):
        field_label = self.google_schema._meta.get_field("client_email").verbose_name
        self.assertEqual(field_label, "client email")

    def test_client_email_max_length(self):
        max_length = self.google_schema._meta.get_field("client_email").max_length
        self.assertEqual(max_length, 255)

    def test_client_x509_cert_url_label(self):
        field_label = self.google_schema._meta.get_field(
            "client_x509_cert_url"
        ).verbose_name
        self.assertEqual(field_label, "client x509 cert url")

    def test_client_x509_cert_url_max_length(self):
        max_length = self.google_schema._meta.get_field(
            "client_x509_cert_url"
        ).max_length
        self.assertEqual(max_length, 255)

    def test_client_x509_cert_url_type_urlfield(self):
        self.assertEqual(
            type(
                self.google_schema._meta.get_field("auth_provider_x509_cert_url")
            ).__name__,
            "URLField",
        )

    def test_delegate_label(self):
        field_label = self.google_schema._meta.get_field("delegate").verbose_name
        self.assertEqual(field_label, "delegate")

    def test_delegate_max_length(self):
        max_length = self.google_schema._meta.get_field("delegate").max_length
        self.assertEqual(max_length, 255)

    def test_delegate_help_text(self):
        help_text = self.google_schema._meta.get_field("delegate").help_text
        self.assertEqual(
            help_text,
            "User account to impersonate when accessing Google. User must have rights to the resources needed.",
        )

    def test_target_label(self):
        field_label = self.google_schema._meta.get_field("target").verbose_name
        self.assertEqual(field_label, "target")

    def test_target_max_length(self):
        max_length = self.google_schema._meta.get_field("target").max_length
        self.assertEqual(max_length, 255)

    def test_target_help_text(self):
        help_text = self.google_schema._meta.get_field("target").help_text
        self.assertEqual(
            help_text,
            "Google domain name to connect to (e.g. my.site.com)",
        )

    ### Functions ###
    def test___str__(self):
        google_schema = GoogleServiceAccountConfigFactory(
            private_key_id="test_project_id"
        )
        self.assertEqual(
            google_schema.__str__(),
            f"{google_schema.project_id}",
        )

    def test_get_absolute_url(self):
        self.assertEqual(
            self.google_schema.get_absolute_url(),
            "/googlesync/serviceaccount/",
        )


class GoogleCustomSchemaTest(TestCase):
    # service_account_config
    def test_service_account_config_foreign_key(self):
        self.assertEqual(
            GoogleCustomSchema._meta.get_field("service_account_config").related_model,
            GoogleServiceAccountConfig,
        )

    # schema_id
    def test_schema_id_label(self):
        field_label = GoogleCustomSchema._meta.get_field("schema_id").verbose_name
        self.assertEqual(field_label, "schema id")

    def test_schema_id_max_length(self):
        max_length = GoogleCustomSchema._meta.get_field("schema_id").max_length
        self.assertEqual(max_length, 255)

    # schema_name
    def test_schema_name_label(self):
        field_label = GoogleCustomSchema._meta.get_field("schema_name").verbose_name
        self.assertEqual(field_label, "schema name")

    def test_schema_name_max_length(self):
        max_length = GoogleCustomSchema._meta.get_field("schema_name").max_length
        self.assertEqual(max_length, 255)

    # display_name
    def test_display_name_label(self):
        field_label = GoogleCustomSchema._meta.get_field("display_name").verbose_name
        self.assertEqual(field_label, "display name")

    def test_display_name_max_length(self):
        max_length = GoogleCustomSchema._meta.get_field("display_name").max_length
        self.assertEqual(max_length, 255)

    # kind
    def test_kind_label(self):
        field_label = GoogleCustomSchema._meta.get_field("kind").verbose_name
        self.assertEqual(field_label, "kind")

    def test_kind_max_length(self):
        max_length = GoogleCustomSchema._meta.get_field("kind").max_length
        self.assertEqual(max_length, 255)

    # etag
    def test_etag_label(self):
        field_label = GoogleCustomSchema._meta.get_field("etag").verbose_name
        self.assertEqual(field_label, "etag")

    def test_etag_max_length(self):
        max_length = GoogleCustomSchema._meta.get_field("etag").max_length
        self.assertEqual(max_length, 255)


class GoogleCustomSchemaFieldTest(TestCase):
    # schema
    def test_schema_foreign_key(self):
        self.assertEqual(
            GoogleCustomSchemaField._meta.get_field("schema").related_model,
            GoogleCustomSchema,
        )

    # field_name
    def test_field_name_label(self):
        field_label = GoogleCustomSchemaField._meta.get_field("field_name").verbose_name
        self.assertEqual(field_label, "field name")

    def test_field_name_max_length(self):
        max_length = GoogleCustomSchemaField._meta.get_field("field_name").max_length
        self.assertEqual(max_length, 255)

    # field_id
    def test_field_id_label(self):
        field_label = GoogleCustomSchemaField._meta.get_field("field_id").verbose_name
        self.assertEqual(field_label, "field id")

    def test_field_id_max_length(self):
        max_length = GoogleCustomSchemaField._meta.get_field("field_id").max_length
        self.assertEqual(max_length, 255)

    # field_type
    def test_field_type_label(self):
        field_label = GoogleCustomSchemaField._meta.get_field("field_type").verbose_name
        self.assertEqual(field_label, "field type")

    def test_field_type_max_length(self):
        max_length = GoogleCustomSchemaField._meta.get_field("field_type").max_length
        self.assertEqual(max_length, 255)

    # multi_valued
    def test_multi_valued_label(self):
        field_label = GoogleCustomSchemaField._meta.get_field(
            "multi_valued"
        ).verbose_name
        self.assertEqual(field_label, "multi valued")

    def test_multi_valued_default(self):
        default = GoogleCustomSchemaField._meta.get_field("multi_valued").default
        self.assertFalse(default, msg="multi_valued defualt is expected to be False")

    # kind
    def test_kind_label(self):
        field_label = GoogleCustomSchemaField._meta.get_field("kind").verbose_name
        self.assertEqual(field_label, "kind")

    def test_kind_max_length(self):
        max_length = GoogleCustomSchemaField._meta.get_field("kind").max_length
        self.assertEqual(max_length, 255)

    # etag
    def test_etag_label(self):
        field_label = GoogleCustomSchemaField._meta.get_field("etag").verbose_name
        self.assertEqual(field_label, "etag")

    def test_etag_max_length(self):
        max_length = GoogleCustomSchemaField._meta.get_field("etag").max_length
        self.assertEqual(max_length, 255)

    # indexed
    def test_indexed_label(self):
        field_label = GoogleCustomSchemaField._meta.get_field("indexed").verbose_name
        self.assertEqual(field_label, "indexed")

    def test_indexed_default(self):
        default = GoogleCustomSchemaField._meta.get_field("indexed").default
        self.assertFalse(default, msg="indexed defualt is expected to be False")

    # display_name
    def test_display_name_label(self):
        field_label = GoogleCustomSchemaField._meta.get_field(
            "display_name"
        ).verbose_name
        self.assertEqual(field_label, "display name")

    def test_display_name_max_length(self):
        max_length = GoogleCustomSchemaField._meta.get_field("display_name").max_length
        self.assertEqual(max_length, 255)

    # read_access_type
    def test_read_access_type_label(self):
        field_label = GoogleCustomSchemaField._meta.get_field(
            "read_access_type"
        ).verbose_name
        self.assertEqual(field_label, "read access type")

    def test_read_access_type_max_length(self):
        max_length = GoogleCustomSchemaField._meta.get_field(
            "read_access_type"
        ).max_length
        self.assertEqual(max_length, 255)

    # numeric_indexing_spec_min_value
    def numeric_indexing_spec_min_value_optional(self):
        blank = GoogleCustomSchemaField._meta.get_field(
            "numeric_indexing_spec_min_value"
        ).blank
        null = GoogleCustomSchemaField._meta.get_field(
            "numeric_indexing_spec_min_value"
        ).null
        self.assertTrue(blank)
        self.assertTrue(null)

    # numeric_indexing_spec_max_value
    def numeric_indexing_spec_max_value_optional(self):
        blank = GoogleCustomSchemaField._meta.get_field(
            "numeric_indexing_spec_max_value"
        ).blank
        null = GoogleCustomSchemaField._meta.get_field(
            "numeric_indexing_spec_max_value"
        ).null
        self.assertTrue(blank)
        self.assertTrue(null)

    ### Functions ###
    @patch.object(GoogleCustomSchemaField, "__str__")
    def test___str__(self, mock___str___command):
        mock___str___command.return_value = "dot.notation.example"
        custom_schema_field = GoogleCustomSchemaFieldFactory()

        self.assertEqual(str(custom_schema_field), "dot.notation.example")

    def test_get_type(self):
        regular_BOOL = GoogleCustomSchemaFieldFactory(
            etag="custom_etag", field_type="BOOL"
        )
        regular_DATE = GoogleCustomSchemaFieldFactory(
            etag="custom_etag", field_type="DATE"
        )
        regular_DOUBLE = GoogleCustomSchemaFieldFactory(
            etag="custom_etag", field_type="DOUBLE"
        )
        regular_EMAIL = GoogleCustomSchemaFieldFactory(
            etag="custom_etag", field_type="EMAIL"
        )
        regular_INT64 = GoogleCustomSchemaFieldFactory(
            etag="custom_etag", field_type="INT64"
        )
        regular_PHONE = GoogleCustomSchemaFieldFactory(
            etag="custom_etag", field_type="PHONE"
        )
        regular_STRING = GoogleCustomSchemaFieldFactory(
            etag="custom_etag", field_type="STRING"
        )

        self.assertEqual(regular_BOOL.get_type(), bool)
        self.assertEqual(regular_DATE.get_type(), datetime)
        self.assertEqual(regular_DOUBLE.get_type(), float)
        self.assertEqual(regular_EMAIL.get_type(), str)
        self.assertEqual(regular_INT64.get_type(), int)
        self.assertEqual(regular_PHONE.get_type(), str)
        self.assertEqual(regular_STRING.get_type(), str)


class GoogleDefaultSchemaTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        GoogleDefaultSchemaFactory(schema_id=1)

    def setUp(self):
        self.google_default_schema = GoogleDefaultSchema.objects.get(schema_id=1)
        self.service_account_config = self.google_default_schema._meta.get_field(
            "service_account_config"
        )
        self.description = self.google_default_schema._meta.get_field("description")
        self.schema_id = self.google_default_schema._meta.get_field("schema_id")
        self.type = self.google_default_schema._meta.get_field("type")

    # service_account_config
    def test_service_account_config_foreign_key(self):
        self.assertEqual(
            self.service_account_config.related_model,
            GoogleServiceAccountConfig,
        )

    # description
    def test_description_label(self):
        field_label = self.description.verbose_name
        self.assertEqual(field_label, "description")

    def test_description_max_length(self):
        max_length = self.description.max_length
        self.assertEqual(max_length, 1024)

    def test_description_optional(self):
        blank = self.description.blank
        null = self.description.null
        self.assertTrue(blank)
        self.assertTrue(null)

    # schema_id
    def test_schema_id_label(self):
        field_label = self.schema_id.verbose_name
        self.assertEqual(field_label, "schema id")

    def test_schema_id_max_length(self):
        max_length = self.schema_id.max_length
        self.assertEqual(max_length, 255)

    # type
    def test_type_label(self):
        field_label = self.type.verbose_name
        self.assertEqual(field_label, "type")

    def test_type_max_length(self):
        max_length = self.type.max_length
        self.assertEqual(max_length, 255)

    def test___str__(self):
        self.assertEqual(
            self.google_default_schema.__str__(), self.google_default_schema.schema_id
        )


class GoogleDefaultSchemaPropertyTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        GoogleDefaultSchemaPropertyFactory(etag="test")

    def setUp(self):
        self.google_default_schema_property = GoogleDefaultSchemaProperty.objects.get(
            etag="test"
        )
        self.schema = self.google_default_schema_property._meta.get_field("schema")
        self.parent = self.google_default_schema_property._meta.get_field("parent")
        self.etag = self.google_default_schema_property._meta.get_field("etag")
        self.format = self.google_default_schema_property._meta.get_field("format")
        self.type = self.google_default_schema_property._meta.get_field("type")
        self.description = self.google_default_schema_property._meta.get_field(
            "description"
        )

    # schema
    def test_schema_foreign_key(self):
        self.assertEqual(
            self.schema.related_model,
            GoogleDefaultSchema,
        )

    # parent
    def test_parent_foreign_key(self):
        self.assertEqual(
            self.parent.related_model,
            GoogleDefaultSchemaProperty,
        )

    # etag
    def test_etag_label(self):
        field_label = self.etag.verbose_name
        self.assertEqual(field_label, "etag")

    def test_etag_max_length(self):
        max_length = self.etag.max_length
        self.assertEqual(max_length, 255)

    # format
    def test_format_label(self):
        field_label = self.format.verbose_name
        self.assertEqual(field_label, "format")

    def test_format_max_length(self):
        max_length = self.format.max_length
        self.assertEqual(max_length, 255)

    def test_format_optional(self):
        blank = self.format.blank
        null = self.format.null
        self.assertTrue(blank)
        self.assertTrue(null)

    # type
    def test_type_label(self):
        field_label = self.type.verbose_name
        self.assertEqual(field_label, "type")

    def test_type_max_length(self):
        max_length = self.type.max_length
        self.assertEqual(max_length, 255)

    def test_type_optional(self):
        blank = self.type.blank
        null = self.type.null
        self.assertTrue(blank)
        self.assertTrue(null)

    # description
    def test_description_label(self):
        field_label = self.description.verbose_name
        self.assertEqual(field_label, "description")

    def test_description_max_length(self):
        max_length = self.description.max_length
        self.assertEqual(max_length, 1024)

    def test_description_optional(self):
        blank = self.description.blank
        null = self.description.null
        self.assertTrue(blank)
        self.assertTrue(null)

    ### Functions ###
    def test___str__(self):
        with patch.object(
            GoogleDefaultSchemaProperty,
            "dot_notation",
            "test.dot.notation",
        ):
            default_schema_property = GoogleDefaultSchemaPropertyFactory()
            test = default_schema_property.__str__()
            self.assertEqual(test, "test.dot.notation")

    def test_is_custom(self):
        custom_parent = GoogleDefaultSchemaPropertyFactory(etag="customSchemas")
        regular = GoogleDefaultSchemaPropertyFactory(etag="test")
        custom = GoogleDefaultSchemaPropertyFactory(
            etag="test_custom", parent=custom_parent
        )
        self.assertTrue(custom.is_custom)
        self.assertFalse(regular.is_custom)

    def test_get_custom_field(self):
        custom_schema_field = GoogleCustomSchemaFieldFactory(etag="custom_etag")
        custom_parent = GoogleDefaultSchemaPropertyFactory(etag="customSchemas")
        regular = GoogleDefaultSchemaPropertyFactory(etag="custom_etag")
        custom = GoogleDefaultSchemaPropertyFactory(
            etag="custom_etag", parent=custom_parent
        )
        self.assertIsNone(regular.get_custom_field())
        self.assertEqual(custom.get_custom_field(), custom_schema_field)

    def test_dot_notation(self):

        default_schema = GoogleDefaultSchemaFactory(schema_id="schema_id")
        default_schema_property = GoogleDefaultSchemaPropertyFactory(
            etag="customSchemas", schema=default_schema
        )
        custom_schema = GoogleCustomSchemaFactory(
            schema_id="custom_schema_id", schema_name="custom_schema_name"
        )
        custom_schema_field = GoogleCustomSchemaFieldFactory(
            schema=custom_schema, etag="custom_etag", field_name="custom_field_name"
        )
        with patch.object(
            default_schema_property, "get_custom_field", custom_schema_field
        ):
            regular = GoogleDefaultSchemaPropertyFactory(etag="custom_etag")

            custom = GoogleDefaultSchemaPropertyFactory(
                etag="custom_etag", parent=default_schema_property
            )

            self.assertEqual(regular.dot_notation, "custom_etag")
            self.assertEqual(
                custom.dot_notation,
                "customSchemas.custom_schema_name.custom_field_name",
            )

    def test_get_type(self):
        custom_schema_field = GoogleCustomSchemaFieldFactory(etag="custom_etag")
        custom_parent = GoogleDefaultSchemaPropertyFactory(etag="customSchemas")
        regular_string = GoogleDefaultSchemaPropertyFactory(
            etag="custom_etag", type="string"
        )
        regular_boolean = GoogleDefaultSchemaPropertyFactory(
            etag="custom_etag", type="boolean"
        )
        regular_array = GoogleDefaultSchemaPropertyFactory(
            etag="custom_etag", type="array"
        )
        regular_any = GoogleDefaultSchemaPropertyFactory(etag="custom_etag", type="any")

        default_schema_property = GoogleDefaultSchemaPropertyFactory(
            etag="custom_etag", parent=custom_parent
        )

        self.assertEqual(regular_string.get_type(), str)
        self.assertEqual(regular_boolean.get_type(), bool)
        self.assertEqual(regular_array.get_type(), list)
        self.assertEqual(regular_any.get_type(), Any)

        my_mock_type = mock.Mock()
        my_mock = mock.Mock(**{"get_type": my_mock_type})
        with patch.object(
            default_schema_property,
            "get_custom_field",
            return_value=my_mock,
        ):
            test = default_schema_property.get_type()
            my_mock.get_type.assert_called()


class GoogleDeviceTest(TestCase):
    pass


class GoogleSyncProfileAbstractTest(TestCase):
    def test_is_abstract(self):
        self.assertTrue(GoogleConfigAbstract._meta.abstract)

    def test_name_label(self):
        field_label = GoogleSyncProfileAbstract._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")

    def test_name_max_length(self):
        max_length = GoogleSyncProfileAbstract._meta.get_field("name").max_length
        self.assertEqual(max_length, 255)

    def test_google_schema_foreign_key(self):
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


class MappingAbstractTest(TestCase):
    def test_is_abstract(self):
        self.assertTrue(MappingAbstract._meta.abstract)

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

    def test_matching_priority_optional(self):
        self.assertEqual(
            MappingAbstract._meta.get_field("matching_priority").blank, True
        )
        self.assertEqual(
            MappingAbstract._meta.get_field("matching_priority").null, True
        )

    def test_unique_constraints(self):
        expected_constraint_fields = [
            ("sync_profile", "to_field"),
            ("sync_profile", "matching_priority"),
        ]
        constraints = [
            c
            for c in MappingAbstract._meta.constraints
            if isinstance(c, UniqueConstraint)
        ]
        self.assertEqual(
            len(expected_constraint_fields),
            len(constraints),
            "Difference in unique constraint length.",
        )
        for constraint in constraints:
            self.assertIn(constraint.fields, expected_constraint_fields)

    ### Functions ###
    @patch("googlesync.models.MappingAbstract._meta.abstract", set())
    @patch("googlesync.models.MappingAbstract.sync_profile", "profile_name")
    # @patch("googlesync.models.MappingAbstract.sync_profile", "from_field", create=True)
    # @patch("googlesync.models.MappingAbstract")
    def test___str__(self):
        # mock_mapping_abstract.from_field = "from_field"

        mapping_abstract = MappingAbstract(to_field="to field")
        with patch.object(
            mapping_abstract,
            "from_field",
            "from field",
            create=True,
        ):

            # print(mock_mapping_abstract.from_field)
            # self.assertEqual(mock_mapping_abstract.from_field, "from_field")
            # mock_mapping_abstract = MagicMock(MappingAbstract)
            ## with patch.object(MappingAbstract) as a:
            # mock_mapping_abstract.from_field = "from field"
            # mock_mapping_abstract.to_field = "to field"
            # mock_mapping_abstract.sync_profile = "profile_name"
            # mock_mapping_abstract.from_field.name.return_value = "from field"
            # google_default_schema_property = GoogleDefaultSchemaProperty()
            # google_person_mapping = MappingAbstract(to_field="to field")
            self.assertEqual(
                mapping_abstract.__str__(),
                "profile_name: from field => to field",
            )


class GooglePersonMappingTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        GooglePersonMappingFactory()

    def setUp(self):
        self.google_person_mapping = GooglePersonMapping.objects.get(id=1)

    def test_subclass(self):
        self.assertTrue(issubclass(GooglePersonMapping, MappingAbstract))

    # sync_profile
    def test_sync_profile_foreign_key(self):
        self.assertEqual(
            self.google_person_mapping._meta.get_field("sync_profile").related_model,
            GooglePersonSyncProfile,
        )

    # from_field
    def test_from_field_foreign_key(self):
        self.assertEqual(
            self.google_person_mapping._meta.get_field("from_field").related_model,
            GoogleDefaultSchemaProperty,
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

    # sync_profile
    def test_sync_profile_foreign_key(self):
        self.assertEqual(
            self.google_device_mapping._meta.get_field("sync_profile").related_model,
            GoogleDeviceSyncProfile,
        )

    # from_field
    def test_from_field_foreign_key(self):
        self.assertEqual(
            self.google_device_mapping._meta.get_field("from_field").related_model,
            GoogleDefaultSchemaProperty,
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


class GoogleDeviceLinkMappingTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        GoogleDeviceLinkMappingFactory()

    def setUp(self):
        self.google_device_link_mapping = GoogleDeviceLinkMapping.objects.get(id=1)

    def test_subclass(self):
        self.assertTrue(issubclass(GoogleDeviceLinkMapping, MappingAbstract))

    def test_sync_profile_foreign_key(self):
        self.assertEqual(
            self.google_device_link_mapping._meta.get_field(
                "sync_profile"
            ).related_model,
            GoogleDeviceSyncProfile,
        )

    def test_to_field_label(self):
        field_label = self.google_device_link_mapping._meta.get_field(
            "to_field"
        ).verbose_name
        self.assertEqual(field_label, "to field")

    def test_to_field_max_length(self):
        max_length = self.google_device_link_mapping._meta.get_field(
            "to_field"
        ).max_length
        self.assertEqual(max_length, 255)

    def test_to_field_choices(self):
        choices = self.google_device_link_mapping._meta.get_field("to_field").choices
        potential_choices = [
            (f.name, f.verbose_name) for f in Device._meta.fields if f.name != "id"
        ]
        self.assertCountEqual(potential_choices, choices)

    def test_from_field_choices_not_contain_id(self):
        choices = self.google_device_link_mapping._meta.get_field("from_field").choices
        self.assertNotIn(("id", "id"), choices)

    def test_from_field_choices(self):
        choices = self.google_device_link_mapping._meta.get_field("from_field").choices
        potential_choices = [
            (f.name, f.verbose_name)
            for f in GoogleDevice._meta.fields
            if f.name != "id"
        ]
        self.assertCountEqual(potential_choices, choices)


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
