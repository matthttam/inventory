from datetime import datetime
from typing import Any

from devices.models import Device
from django.db import models
from django.db.models import Q
from django.urls import reverse
from locations.models import Building
from people.models import Person, PersonType


class GoogleConfigAbstract(models.Model):
    client_id = models.CharField(max_length=255)
    project_id = models.CharField(max_length=255)
    auth_uri = models.URLField(
        max_length=255, default="https://accounts.google.com/o/oauth2/auth"
    )
    token_uri = models.URLField(
        max_length=255, default="https://oauth2.googleapis.com/token"
    )
    auth_provider_x509_cert_url = models.URLField(
        max_length=255, default="https://www.googleapis.com/oauth2/v1/certs"
    )

    class Meta:
        abstract = True


class GoogleConfig(GoogleConfigAbstract):

    client_secret = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.project_id}"

    def get_absolute_url(self):
        return reverse("googlesync:config", kwargs={})


class GoogleServiceAccountConfig(GoogleConfigAbstract):
    type = models.CharField(max_length=255, default="service_account")
    private_key_id = models.CharField(max_length=255)
    private_key = models.TextField(max_length=2048)
    client_email = models.EmailField(max_length=255)
    client_x509_cert_url = models.URLField(max_length=255)
    delegate = models.EmailField(
        max_length=255,
        help_text="User account to impersonate when accessing Google. User must have rights to the resources needed.",
    )
    target = models.CharField(
        max_length=255, help_text="Google domain name to connect to (e.g. my.site.com)"
    )
    person_initialized = models.BooleanField(default=False)
    device_initialized = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.project_id}"

    def get_absolute_url(self):
        return reverse("googlesync:service_account_config", kwargs={})


class GoogleCustomSchema(models.Model):
    """
    {
       "schemaId": string,
       "schemaName": string,
       "fields": [
           {
           object (SchemaFieldSpec)
           }
       ],
       "displayName": string,
       "kind": string,
       "etag": string
    }
    """

    service_account_config = models.ForeignKey(
        GoogleServiceAccountConfig,
        on_delete=models.CASCADE,
        related_name="custom_schemas",
    )
    schema_id = models.CharField(max_length=255)
    schema_name = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255)
    kind = models.CharField(max_length=255)
    etag = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.schema_name}"


class GoogleCustomSchemaField(models.Model):
    """
    SchemaFieldSpec
    {
       "fieldName": string,
       "fieldId": string,
       "fieldType": string,
       "multiValued": boolean,
       "kind": string,
       "etag": string,
       "indexed": boolean,
       "displayName": string,
       "readAccessType": string,
       "numericIndexingSpec": {
           "minValue": number,
           "maxValue": number
       }
    }
    """

    schema = models.ForeignKey(
        GoogleCustomSchema, on_delete=models.CASCADE, related_name="fields"
    )
    field_name = models.CharField(max_length=255)
    field_id = models.CharField(max_length=255)
    field_type = models.CharField(max_length=255)
    multi_valued = models.BooleanField(default=False)
    kind = models.CharField(max_length=255)
    etag = models.CharField(max_length=255)
    indexed = models.BooleanField(default=False)
    display_name = models.CharField(max_length=255)
    read_access_type = models.CharField(max_length=255)
    numeric_indexing_spec_min_value = models.IntegerField(blank=True, null=True)
    numeric_indexing_spec_max_value = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.dot_notation

    @property
    def dot_notation(self) -> str:
        """Return a dot notation path for this custom schema field"""
        return f"{self.schema.schema_name}.{self.field_name}"

    def get_type(self):

        if self.field_type == "BOOL":
            return bool
        elif self.field_type == "DATE":
            return datetime
        elif self.field_type == "DOUBLE":
            return float
        elif self.field_type == "EMAIL":
            return str
        elif self.field_type == "INT64":
            return int
        elif self.field_type == "PHONE":
            return str
        elif self.field_type == "STRING":
            return str
        else:
            raise TypeError()


class GoogleDefaultSchema(models.Model):
    """
    {
      "Users": {
           "type": "object",
           "properties": {
               "etag": {
                   "type": "string",
                   "description": "ETag of the collection."
               },
               "kind": {
                   "type": "string",
                   "description": "Output only. The type of the API resource. For Users resources, the value is `admin#directory#user`.",
                   "default": "calendar#acl"
               },
               "nextPageToken": {
                   "type": "string",
                   "description": "Token used to access the next
                   page of this result. Omitted if no further results are available."
               }
           }
       }
    }
    """

    service_account_config = models.ForeignKey(
        GoogleServiceAccountConfig,
        on_delete=models.CASCADE,
        related_name="default_schemas",
    )
    description = models.CharField(max_length=1024, blank=True, null=True)
    schema_id = models.CharField(max_length=255)
    type = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.schema_id}"


class GoogleDefaultSchemaProperty(models.Model):
    schema = models.ForeignKey(
        GoogleDefaultSchema, on_delete=models.CASCADE, related_name="properties"
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="children",
    )
    etag = models.CharField(max_length=255)
    format = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=1024, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Google default schema properties"

    def __str__(self):
        return self.dot_notation

    @property
    def is_custom(self):
        return self.parent and self.parent.etag == "customSchemas"

    def get_custom_field(self):
        return GoogleCustomSchemaField.objects.filter(etag=self.etag).first()

    @property
    def dot_notation(self) -> str:
        """Return a dot notation path for this schema property"""
        parent = self.parent
        if self.is_custom:

            custom_field = self.get_custom_field()
            if custom_field:
                etag = self.get_custom_field().dot_notation
            else:
                etag = self.etag
        else:
            etag = self.etag
        return_string = f"{etag}"
        while parent:
            return_string = f"{parent.etag}.{return_string}"
            parent = parent.parent

        return return_string

    def get_type(self):
        if self.is_custom:
            related_custom_field = self.get_custom_field()
            return related_custom_field.get_type()
        elif self.type == "string":
            return str
        elif self.type == "boolean":
            return bool
        elif self.type == "array":
            return list
        elif self.type == "any":
            """Type is basically unknown and will have to be figured out based on the data"""
            return Any


class GoogleDevice(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    serial_number = models.CharField(max_length=255, blank=True, null=True)
    device_model = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    organization_unit = models.CharField(max_length=255, blank=True, null=True)
    enrollment_time = models.DateTimeField(null=True, blank=True)
    last_policy_sync = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    most_recent_user = models.CharField(max_length=255, blank=True, null=True)
    annotated_asset_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.annotated_asset_id} ({self.serial_number}) - {self.device_model}"


class GoogleSyncProfileAbstract(models.Model):
    name = models.CharField(max_length=255)

    google_service_account_config = models.ForeignKey(
        GoogleServiceAccountConfig, on_delete=models.PROTECT
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.name}"


# Person sync profile
class GooglePersonSyncProfile(GoogleSyncProfileAbstract):
    person_type = models.ForeignKey(PersonType, on_delete=models.PROTECT)
    google_query = models.CharField(
        max_length=1024,
        default="orgUnitPath=/",
        help_text="Google API query to use when searching for users to sync for this profile. (e.g. 'orgUnitPath=/Staff'). Query documentation: https://developers.google.com/admin-sdk/directory/v1/guides/search-users",
        blank=True,
    )
    domain = models.CharField(
        max_length=1024,
        default="",
        blank=True,
        help_text="Filter by domain of users. If left blank users of any domain for your Google Customer will be included.",
    )


class GoogleDeviceSyncProfile(GoogleSyncProfileAbstract):
    google_org_unit_path = models.CharField(
        max_length=1024,
        default="",
        help_text="The full path of the organizational unit (minus the leading /) or its unique ID.",
        blank=True,
    )
    google_query = models.CharField(
        max_length=1024,
        default="",
        help_text="Google API query to use when searching for devices to sync for this profile. (e.g. 'location:seattle'). Query documentation: https://developers.google.com/admin-sdk/directory/v1/list-query-operators",
        blank=True,
    )


class MappingAbstract(models.Model):
    sync_profile = None
    to_field = models.CharField(max_length=255, blank=True, null=True, default=None)
    matching_priority = models.IntegerField(
        choices=[(x, x) for x in range(1, 10)], blank=True, null=True
    )

    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(
                fields=["sync_profile", "to_field"],
                name="u_sync_profile_and_to_field_%(class)s",
            ),
            models.UniqueConstraint(
                fields=["sync_profile", "matching_priority"],
                name="u_sync_profile_and_matching_priority_%(class)s",
            ),
        ]

    def __str__(self):
        return f"{self.sync_profile}: {self.from_field} => {self.to_field}"


class GooglePersonMapping(MappingAbstract):
    sync_profile = models.ForeignKey(
        GooglePersonSyncProfile, on_delete=models.PROTECT, related_name="mappings"
    )
    from_field = models.ForeignKey(
        GoogleDefaultSchemaProperty,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        default=None,
    )
    to_field = models.CharField(
        max_length=255,
        choices=[
            (f.name, f.verbose_name) for f in Person._meta.fields if f.name != "id"
        ],  # When we support m2m field mappings use: for f in (list(Person._meta.fields) + list(Person._meta.local_many_to_many))
    )

    def get_absolute_url(self):
        return reverse("googlesync:person_mapping", kwargs={"pk": self.pk})

    def get_type(self):
        return self.from_field.get_type()


class GoogleDeviceMapping(MappingAbstract):
    sync_profile = models.ForeignKey(
        GoogleDeviceSyncProfile, on_delete=models.PROTECT, related_name="mappings"
    )
    from_field = models.ForeignKey(
        GoogleDefaultSchemaProperty,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        default=None,
        limit_choices_to=Q(schema__schema_id="ChromeOsDevice"),
    )
    to_field = models.CharField(
        max_length=255,
        choices=[(f.name, f.verbose_name) for f in GoogleDevice._meta.fields],
    )

    def get_absolute_url(self):
        return reverse("googlesync:device_mapping", kwargs={"pk": self.pk})


class GoogleDeviceLinkMapping(MappingAbstract):
    sync_profile = models.ForeignKey(
        GoogleDeviceSyncProfile, on_delete=models.PROTECT, related_name="link_mappings"
    )

    from_field = models.CharField(
        max_length=255,
        choices=[
            (f.name, f.verbose_name)
            for f in GoogleDevice._meta.fields
            if f.name != "id"
        ],
    )

    to_field = models.CharField(
        max_length=255,
        choices=[
            (f.name, f.verbose_name) for f in Device._meta.fields if f.name != "id"
        ],
    )


class TranslationAbstract(models.Model):
    translate_from = models.CharField(max_length=255)
    translate_to = models.CharField(max_length=255)

    class Meta:
        abstract = True


class GooglePersonTranslation(TranslationAbstract):
    google_person_mapping = models.ForeignKey(
        GooglePersonMapping,
        on_delete=models.CASCADE,
        default=1,
        related_name="translations",
    )

    def __str__(self):
        return f"Translate {self.google_person_mapping.to_field!r} from {self.translate_from!r} to {self.translate_to!r}"


class GoogleDeviceTranslation(TranslationAbstract):
    google_device_mapping = models.ForeignKey(
        GoogleDeviceMapping,
        on_delete=models.CASCADE,
        default=1,
        related_name="translations",
    )

    def __str__(self):
        return f"Translate {self.google_device_mapping.to_field!r} from {self.translate_from!r} to {self.translate_to!r}"


class DeviceBuildingToGoogleOUMapping(models.Model):
    person_type = models.ForeignKey(
        PersonType, on_delete=models.PROTECT, blank=True, null=True
    )
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    organization_unit = models.CharField(max_length=1024)
