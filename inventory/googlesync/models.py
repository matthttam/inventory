from django.db import models
from django.urls import reverse
from people.models import Person, PersonType
from devices.models import Device


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
    client_email = models.CharField(max_length=255)
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


# Person sync profile
class GooglePersonSyncProfile(models.Model):
    name = models.CharField(max_length=255)
    person_type = models.ForeignKey(PersonType, on_delete=models.PROTECT)
    google_service_account_config = models.ForeignKey(
        GoogleServiceAccountConfig, on_delete=models.PROTECT
    )
    google_query = models.CharField(
        max_length=1024,
        default="orgUnitPath=/",
        help_text="Google API query to use when searching for users to sync for this profile. (e.g. 'orgUnitPath=/Staff'). Query documentation: https://developers.google.com/admin-sdk/directory/v1/guides/search-users",
        blank=True,
    )

    def __str__(self):
        return f"{self.name} ({self.person_type}: {self.google_service_account_config})"


class GooglePersonMapping(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["google_person_sync_profile", "person_field"],
                name="unique_google_person_sync_profile_and_person_field",
            )
        ]

    google_person_sync_profile = models.ForeignKey(
        GooglePersonSyncProfile, on_delete=models.PROTECT
    )
    google_field = models.CharField(max_length=255)
    person_field = models.CharField(
        max_length=255,
        choices=[
            (f.name, f.verbose_name) for f in Person._meta.fields if f.name != "id"
        ],
    )
    matching_priority = models.IntegerField(
        choices=[(x, x) for x in range(1, 10)], unique=True, blank=True, null=True
    )

    def __str__(self):
        return f"{self.google_field} => {self.person_field}"

    def get_absolute_url(self):
        return reverse("googlesync:person_mapping", kwargs={})


class GooglePersonTranslation(models.Model):
    google_person_mapping = models.ForeignKey(
        GooglePersonMapping, on_delete=models.CASCADE, default=1
    )
    translate_from = models.CharField(max_length=255)
    translate_to = models.CharField(max_length=255)

    def __str__(self):
        return f"Translate {self.google_person_mapping.person_field!r} from {self.translate_from!r} to {self.translate_to!r}"


# Device Sync Settings
class GoogleDeviceSyncProfile(models.Model):
    name = models.CharField(max_length=255)
    google_service_account_config = models.ForeignKey(
        GoogleServiceAccountConfig, on_delete=models.PROTECT
    )
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


class GoogleDeviceMapping(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["google_device_sync_profile", "device_field"],
                name="unique_google_device_sync_profile_and_device_field",
            )
        ]

    google_device_sync_profile = models.ForeignKey(
        GoogleDeviceSyncProfile, on_delete=models.PROTECT
    )
    google_field = models.CharField(max_length=255)
    device_field = models.CharField(
        max_length=255,
        choices=[
            (f.name, f.verbose_name) for f in Device._meta.fields if f.name != "id"
        ],
    )
    matching_priority = models.IntegerField(
        choices=[(x, x) for x in range(1, 10)], unique=True, blank=True, null=True
    )

    def __str__(self):
        return f"{self.google_field} => {self.device_field}"

    def get_absolute_url(self):
        return reverse("googlesync:device_mapping", kwargs={})


class GoogleDeviceTranslation(models.Model):
    google_device_mapping = models.ForeignKey(
        GoogleDeviceMapping, on_delete=models.CASCADE, default=1
    )

    translate_from = models.CharField(max_length=255)
    translate_to = models.CharField(max_length=255)

    def __str__(self):
        return f"Translate {self.google_device_mapping.device_field!r} from {self.translate_from!r} to {self.translate_to!r}"


class GoogleDevice(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    serial_number = models.CharField(max_length=255, unique=True, blank=True)
    device_model = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=255, blank=True)
    organization_unit = models.CharField(max_length=255, blank=True)
    enrollment_time = models.DateTimeField(null=True, blank=True)
    last_policy_sync = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=255, blank=True)
    most_recent_user = models.CharField(max_length=255, blank=True)
    annotated_asset_id = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.annotated_asset_id} ({self.serial_number}) - {self.device_model}"
