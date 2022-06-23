from django.db import models
from django.urls import reverse
from locations.models import Room, Building
# Create your models here.


class Device(models.Model):
    serial_number = models.CharField(max_length=255, unique=True)
    asset_id = models.CharField(max_length=255, unique=True)
    notes = models.CharField(max_length=255, blank=True)
    status = models.ForeignKey("DeviceStatus", on_delete=models.PROTECT)
    google_id = models.CharField(max_length=255, blank=True)
    google_status = models.CharField(max_length=255, blank=True)
    google_organization_unit = models.CharField(max_length=255, blank=True)
    google_enrollment_time = models.DateTimeField(null=True, blank=True)
    google_last_policy_sync = models.DateTimeField(null=True, blank=True)
    google_location = models.CharField(max_length=255, blank=True)
    google_most_recent_user = models.CharField(max_length=255, blank=True)
    device_model = models.ForeignKey("DeviceModel", on_delete=models.PROTECT)
    building = models.ForeignKey(
        Building, on_delete=models.SET_NULL, null=True, blank=True)
    room = models.ForeignKey(
        Room, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.asset_id} ({self.serial_number}) - {self.device_model}"

    def get_absolute_url(self):
        return reverse('devices:detail', kwargs={'pk': self.pk})

    def location(self):
        return self.room

    def display_name(self):
        if self.asset_id:
            return f"{self.asset_id} ({self.serial_number})"
        else:
            return f"{self.serial_number}"


class DeviceAccessory(models.Model):
    name = models.CharField(max_length=255)
    device_model = models.ManyToManyField("DeviceModel")


class DeviceModel(models.Model):
    name = models.CharField(max_length=255)
    manufacturer = models.ForeignKey(
        "DeviceManufacturer", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.manufacturer} {self.name}"


class DeviceManufacturer(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


class DeviceStatus(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Device statuses"

    def __str__(self):
        return f"{self.name}"
