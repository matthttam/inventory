from django.db import models
from django.contrib.auth.models import User
from timezone_field import TimeZoneField
from inventory.settings import TIME_ZONE as default_timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    timezone = TimeZoneField(default=default_timezone)
