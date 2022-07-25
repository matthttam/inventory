from django.db import models
from django.urls import reverse
from locations.models import Room, Building


class DeviceStatus(models.Model):
    name = models.CharField(max_length=255, unique=True)
    is_inactive = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Device statuses"

    def __str__(self):
        return f"{self.name}"


class DeviceManufacturer(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


class DeviceModel(models.Model):
    name = models.CharField(max_length=255)
    manufacturer = models.ForeignKey("DeviceManufacturer", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.manufacturer} {self.name}"


class Device(models.Model):
    serial_number = models.CharField(max_length=255, unique=True)
    asset_id = models.CharField(max_length=255, unique=True, blank=True)
    notes = models.CharField(max_length=255, blank=True)
    status = models.ForeignKey(DeviceStatus, on_delete=models.PROTECT)
    device_model = models.ForeignKey(DeviceModel, on_delete=models.PROTECT)
    building = models.ForeignKey(
        Building, on_delete=models.SET_NULL, null=True, blank=True
    )
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)
    google_device = models.OneToOneField(
        "googlesync.GoogleDevice",
        on_delete=models.SET_NULL,
        default=None,
        blank=True,
        null=True,
    )

    def __str__(self):
        if self.asset_id:
            return f"{self.asset_id} ({self.serial_number})"
        return f"{self.serial_number}"

    def get_absolute_url(self):
        return reverse("devices:detail", kwargs={"pk": self.pk})

    def display_name(self):
        return f"{self} - {self.device_model}"


class DeviceAccessory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    device_models = models.ManyToManyField(DeviceModel)

    def __str__(self):
        # return f"{self.manufacturer} {self.name}"
        device_model_names = ",".join([x.name for x in self.device_models.all()])
        return f"{self.name} ({device_model_names})"
