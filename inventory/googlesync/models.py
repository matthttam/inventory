from email.policy import default
from django.db import models
from django.urls import reverse
from people.models import Person, PersonType


class GoogleConfig(models.Model):
    client_id = models.CharField(max_length=255)
    project_id = models.CharField(max_length=255)
    auth_uri = models.CharField(
        max_length=255, default="https://accounts.google.com/o/oauth2/auth"
    )
    token_uri = models.CharField(
        max_length=255, default="https://oauth2.googleapis.com/token"
    )
    auth_provider_x09_cert_url = models.CharField(
        max_length=255, default="https://www.googleapis.com/oauth2/v1/certs"
    )
    client_secret = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.project_id}"

    def get_absolute_url(self):
        return reverse("googlesync:config", kwargs={})


class GoogleServiceAccountConfig(models.Model):
    type = models.CharField(max_length=255, default="service_account")
    project_id = models.CharField(max_length=255)
    private_key_id = models.CharField(max_length=255)
    private_key = models.TextField(max_length=2048)
    client_email = models.CharField(max_length=255)
    client_id = models.CharField(max_length=255)
    auth_uri = models.CharField(
        max_length=255, default="https://accounts.google.com/o/oauth2/auth"
    )
    token_uri = models.CharField(
        max_length=255, default="https://oauth2.googleapis.com/token"
    )
    auth_provider_x09_cert_url = models.CharField(
        max_length=255, default="https://www.googleapis.com/oauth2/v1/certs"
    )
    client_x509_cert_url = models.CharField(max_length=255)
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
    # person_field = models.ForeignKey(
    #    GooglePersonMapping, on_delete=models.PROTECT, to_field="person_field"
    # )
    translate_from = models.CharField(max_length=255)
    translate_to = models.CharField(max_length=255)

    def __str__(self):
        return f"Translate {self.google_person_mapping.person_field!r} from {self.translate_from!r} to {self.translate_to!r}"
