import json
from typing import Type

import googleapiclient.discovery
from django.core.management.base import BaseCommand
from django.db.models import Count
from django.forms import model_to_dict
from google.oauth2 import service_account
from googlesync.exceptions import ConfigNotFound
from googlesync.models import (
    GoogleCustomSchema,
    GoogleCustomSchemaField,
    GoogleDefaultSchema,
    GoogleDefaultSchemaProperty,
    GoogleServiceAccountConfig,
    GoogleSyncProfileAbstract,
)


class GoogleSyncCommandAbstract(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Get the google config
        self.google_config = self._get_google_config_dict()
        self.DELEGATE = self.google_config.pop("delegate")

        # Retreive current customer information used by other services
        self.customer = self._get_my_customer()

    def _get_google_config_dict(self) -> dict:
        try:
            google_config = model_to_dict(self._get_google_config())
        except AttributeError:
            self.stdout.write(self.style.ERROR("Failed to find google sync config!"))
            raise ConfigNotFound(config_name="Google Sync")

        return google_config

    def _get_google_config(self) -> GoogleServiceAccountConfig:
        return GoogleServiceAccountConfig.objects.first()

    def _get_google_credentials(self, scopes: list):
        # Parse the config into a json string and load it into a json object
        credentials = service_account.Credentials.from_service_account_info(
            json.loads(json.dumps(self.google_config)), scopes=scopes
        )
        credentials_delegated = credentials.with_subject(self.DELEGATE)
        return credentials_delegated

    def _get_my_customer(self):
        customer_resource = self._get_customer_service()
        request = customer_resource.get(customerKey="my_customer")
        return request.execute()

    def _get_customer_service(self):
        service = self._get_service(
            "https://www.googleapis.com/auth/admin.directory.customer.readonly"
        )

        return service.customers()

    def _get_chromeosdevices_service(self):
        service = self._get_service(
            [
                "https://www.googleapis.com/auth/admin.directory.device.chromeos.readonly",
                "https://www.googleapis.com/auth/admin.directory.device.chromeos",
            ]
        )

        return service.chromeosdevices()

    def _get_users_service(self):
        service = self._get_service(
            "https://www.googleapis.com/auth/admin.directory.user.readonly"
        )
        return service.users()

    def _get_schemas_service(self):
        service = self._get_service(
            "https://www.googleapis.com/auth/admin.directory.userschema.readonly"
        )
        return service.schemas()

    def _get_schema_by_name(self, schema_name: str):
        return self._get_service().resources()._schema.get(schema_name)

    def _get_service(self, scopes: list[str] | str = []):
        """
        Returns a service discovery service with provided scopes

        @params
        scopes: List of strings or a comma separated string of scopes for the service.
        """
        if isinstance(scopes, str):
            scopes = scopes.split(",")
        service = googleapiclient.discovery.build(
            "admin",
            "directory_v1",
            credentials=self._get_google_credentials(scopes=scopes),
        )
        return service

    def _extract_from_dictionary(self, dictionary: dict, keys: list):
        if not keys:
            return None
        value = dictionary
        for key in keys:
            value = value[key]
        return value

    def _map_dictionary(
        self, sync_profile: GoogleSyncProfileAbstract, object_dictionary: dict
    ) -> dict:
        mappings = list(sync_profile.mappings.all())
        map_dict = {}
        for mapping in mappings:
            from_field_type = mapping.from_field.get_type()
            try:
                map_dict[mapping.to_field] = self._extract_from_dictionary(
                    object_dictionary, (mapping.from_field.dot_notation).split(".")
                )
                # Convert result to appropriate type
                map_dict[mapping.to_field] = self._convert_to_type(
                    map_dict[mapping.to_field], from_field_type
                )

            except KeyError:
                map_dict[mapping.to_field] = None

            # Use translations to convert one value to another
            translations = list(mapping.translations.all())

            for translation in translations:
                if map_dict[mapping.to_field] == self._convert_to_type(
                    translation.translate_from, from_field_type
                ):
                    map_dict[mapping.to_field] = translation.translate_to

            # Convert mapped value

        return map_dict

    def _convert_to_type(self, value, type: Type):
        if isinstance(value, type):
            return value
        if value is None:
            return None
        if type == bool:
            return value.lower() in ["true", "yes", "1"]
        if type == list:
            return list(value)
        else:
            return str(value)

    def _initialize_custom_schemas(self, parent_schema, parent_property):
        schemas = self._get_schemas_service()
        request = schemas.list(customerId=self.customer.get("id"))
        response = request.execute()
        google_schemas = response.get("schemas")
        # Populate custom schema data
        for gs in google_schemas:
            current_schema = GoogleCustomSchema.objects.create(
                service_account_config_id=self.google_config.get("id"),
                schema_id=gs.get("schemaId"),
                schema_name=gs.get("schemaName"),
                display_name=gs.get("displayName"),
                kind=gs.get("kind"),
                etag=gs.get("etag"),
            )

            for f in gs.get("fields"):
                GoogleCustomSchemaField.objects.create(
                    schema=current_schema,
                    field_name=f.get("fieldName"),
                    field_id=f.get("fieldId"),
                    field_type=f.get("fieldType"),
                    multi_valued=f.get("multiValued", False),
                    kind=f.get("kind"),
                    etag=f.get("etag"),
                    indexed=f.get("indexed", False),
                    display_name=f.get("displayName"),
                    read_access_type=f.get("readAccessType"),
                    numeric_indexing_spec_min_value=f.get(
                        "numericIndexingSpec", {}
                    ).get("minValue", None),
                    numeric_indexing_spec_max_value=f.get(
                        "numericIndexingSpec", {}
                    ).get("maxValue", None),
                )
                GoogleDefaultSchemaProperty.objects.create(
                    schema=parent_schema,
                    etag=f.get("etag"),
                    parent=parent_property,
                )

    def _delete_default_schemas(self, schema_id):
        GoogleDefaultSchema.objects.filter(schema_id=schema_id).delete()
        GoogleDefaultSchema.objects.all().annotate(
            property_count=Count("properties")
        ).filter(property_count=0).delete()

    def _initialize_default_schema(
        self, schema_id, parent_property: GoogleDefaultSchemaProperty = None
    ):

        """Used to create default schema and handle recursion"""
        schema = self._get_schema_by_name(schema_id)
        current_schema = GoogleDefaultSchema.objects.create(
            service_account_config_id=self.google_config.get("id"),
            schema_id=schema.get("id"),
            description=schema.get("description"),
            type=schema.get("type"),
        )
        for etag, property in schema.get("properties").items():
            current_property = GoogleDefaultSchemaProperty.objects.create(
                schema=current_schema,
                etag=etag,
                type=property.get("type"),
                format=property.get("format"),
                description=property.get("description"),
                parent=parent_property,
            )

            recursive_reference = property.get("$ref")
            if recursive_reference is not None:
                reference = self._initialize_default_schema(
                    recursive_reference, current_property
                )
            if (
                property.get("additionalProperties", {}).get("$ref")
                == "UserCustomProperties"
            ):
                self._initialize_custom_schemas(current_schema, current_property)

        return current_schema
