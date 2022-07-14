from abc import ABC, abstractmethod
from django.db import models
from django.urls import reverse
from people.models import Person, PersonType
from devices.models import Device


class GoogleDevice(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    serial_number = models.CharField(max_length=255, unique=True, blank=True, null=True)
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

    def __str__(self):
        return f"{self.project_id}"

    def get_absolute_url(self):
        return reverse("googlesync:service_account_config", kwargs={})


class GoogleSyncProfileAbstract(models.Model):
    name = models.CharField(max_length=255)

    google_service_account_config = models.ForeignKey(
        GoogleServiceAccountConfig, on_delete=models.PROTECT
    )

    class Meta:
        abstract = True


# Person sync profile
class GooglePersonSyncProfile(GoogleSyncProfileAbstract):
    person_type = models.ForeignKey(PersonType, on_delete=models.PROTECT)
    google_query = models.CharField(
        max_length=1024,
        default="orgUnitPath=/",
        help_text="Google API query to use when searching for users to sync for this profile. (e.g. 'orgUnitPath=/Staff'). Query documentation: https://developers.google.com/admin-sdk/directory/v1/guides/search-users",
        blank=True,
    )

    def __str__(self):
        return f"{self.name} ({self.person_type}: {self.google_service_account_config})"


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

    def __str__(self):
        return f"{self.name} (Devices: {self.google_service_account_config})"


class MappingAbstract(models.Model):
    sync_profile = None
    from_field = models.CharField(max_length=255)
    to_field = models.CharField(max_length=255)
    matching_priority = models.IntegerField(
        choices=[(x, x) for x in range(1, 10)], unique=True, blank=True, null=True
    )

    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(
                fields=["sync_profile", "to_field"],
                name="unique_sync_profile_and_to_field_in_%(class)s",
            )
        ]

    def __str__(self):
        return f"{self.from_field} => {self.to_field}"


class GooglePersonMapping(MappingAbstract):
    sync_profile = models.ForeignKey(
        GooglePersonSyncProfile, on_delete=models.PROTECT, related_name="mappings"
    )
    to_field = models.CharField(
        max_length=255,
        choices=[
            (f.name, f.verbose_name) for f in Person._meta.fields if f.name != "id"
        ],
    )

    def get_absolute_url(self):
        return reverse("googlesync:person_mapping", kwargs={"pk": self.pk})


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


class GoogleDeviceMapping(MappingAbstract):
    sync_profile = models.ForeignKey(
        GoogleDeviceSyncProfile, on_delete=models.PROTECT, related_name="mappings"
    )

    to_field = models.CharField(
        max_length=255,
        choices=[(f.name, f.verbose_name) for f in GoogleDevice._meta.fields],
    )

    def get_absolute_url(self):
        return reverse("googlesync:device_mapping", kwargs={"pk": self.pk})


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
