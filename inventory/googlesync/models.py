from django.db import models
from django.urls import reverse
from people.models import Person


class GoogleConfig(models.Model):
    client_id = models.CharField(max_length=255)
    project_id = models.CharField(max_length=255)
    auth_uri = models.CharField(
        max_length=255, default="https://accounts.google.com/o/oauth2/auth")
    token_uri = models.CharField(
        max_length=255, default="https://oauth2.googleapis.com/token")
    auth_provider_x09_cert_url = models.CharField(
        max_length=255, default="https://www.googleapis.com/oauth2/v1/certs")
    client_secret = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.project_id}"

    def get_absolute_url(self):
        return reverse('googlesync:config', kwargs={})


class GoogleServiceAccountConfig(models.Model):
    type = models.CharField(max_length=255, default="service_account")
    project_id = models.CharField(max_length=255)
    private_key_id = models.CharField(max_length=255)
    private_key = models.TextField(max_length=2048)
    client_email = models.CharField(max_length=255)
    client_id = models.CharField(max_length=255)
    auth_uri = models.CharField(
        max_length=255, default="https://accounts.google.com/o/oauth2/auth")
    token_uri = models.CharField(
        max_length=255, default="https://oauth2.googleapis.com/token")
    auth_provider_x09_cert_url = models.CharField(
        max_length=255, default="https://www.googleapis.com/oauth2/v1/certs")
    client_x509_cert_url = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.project_id}"

    def get_absolute_url(self):
        return reverse('googlesync:service_account_config', kwargs={})


class GooglePersonMapping(models.Model):
    google_field = models.CharField(max_length=255)
    person_field = models.CharField(
        max_length=255, choices=[(f.name, f.verbose_name) for f in Person._meta.fields if f.name != 'id'])
    matching_priority = models.IntegerField(
        choices=[(x, x) for x in range(1, 10)], unique=True)

    def __str__(self):
        return f"{self.google_field} => {self.person_field}"

    def get_absolute_url(self):
        return reverse('googlesync:person_mapping', kwargs={})
