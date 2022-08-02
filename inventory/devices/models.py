from django.db import models
from django.db.models import F, Count, Q, When, Value, Case
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.apps import apps

from auditlog.registry import auditlog
from auditlog.models import AuditlogHistoryField

from locations.models import Room, Building

# from googlesync.models import DeviceBuildingToOUMapping


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


class DeviceManager(models.Manager):
    def active(self):
        return self.filter(status__is_inactive=False)

    def get_queryset(self):
        qs = super().get_queryset()

        # Add a count of current assignments
        qs = qs.annotate(
            current_assignment_count=Count(
                F("deviceassignment"),
                filter=Q(deviceassignment__return_datetime=None),
            )
        )

        # Add is_currently_assigned
        qs = qs.annotate(
            is_currently_assigned=Case(
                When(current_assignment_count__gt=0, then=True),
                default=False,
            )
        )

        # Set if the device is active
        qs = qs.annotate(
            is_active=Case(
                When(status__is_inactive=False, then=True),
                default=False,
            )
        )
        return qs


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
    objects = DeviceManager()
    history = AuditlogHistoryField()

    def __str__(self):
        if self.asset_id:
            return f"{self.asset_id} ({self.serial_number})"
        return f"{self.serial_number}"

    def get_absolute_url(self):
        return reverse("devices:detail", kwargs={"pk": self.pk})

    def display_name(self):
        return f"{self} - {self.device_model}"


@receiver(post_save, sender="assignments.DeviceAssignment")
def device_assignment_actions(sender, instance, update_fields, **kwargs):
    """When assigned to a person the device building should be the person's primary building"""
    person = instance.person
    device = instance.device
    if person.primary_building != "" and person.primary_building != device.building:
        device.building = person.primary_building
        device.save()


@receiver(post_save, sender="devices.Device")
def device_building_change_actions(sender, instance, **kwargs):
    """When updated if the assigned building's mapped OU isn't the same as the google synced OU run a command to fix it."""
    DeviceBuildingToGoogleOUMapping_model = apps.get_model(
        "googlesync.DeviceBuildingToGoogleOUMapping"
    )
    mapping = DeviceBuildingToGoogleOUMapping_model.objects.filter(
        building=instance.building
    ).first()
    if mapping is not None and instance.google_device is not None:
        if mapping.organization_unit != instance.google_device.organization_unit:
            print("update!")


class DeviceAccessory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    device_models = models.ManyToManyField(DeviceModel)

    class Meta:
        verbose_name_plural = "Device accessories"

    def __str__(self):
        # return f"{self.manufacturer} {self.name}"
        device_model_names = ",".join([x.name for x in self.device_models.all()])
        return f"{self.name} ({device_model_names})"


# Audit Log Registrations
auditlog.register(Device)
