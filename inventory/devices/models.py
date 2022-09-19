from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from django.apps import apps
from django.core.management import call_command
from django.db import models
from django.db.models import Case, Count, F, Q, Max, When, Value as V
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from locations.models import Building, Room

# from googlesync.models import DeviceBuildingToOUMapping


class DeviceTag(models.Model):
    name = models.CharField(max_length=255, unique=True)
    active = models.BooleanField(default=True)
    icon = models.ImageField(upload_to="devicetag/")

    def __str__(self):
        return f"{self.name}"


class DeviceStatus(models.Model):
    name = models.CharField(max_length=255, unique=True)
    is_inactive = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Device statuses"

    def __str__(self):
        return f"{self.name}"


class DeviceManufacturer(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.name}"


class DeviceModel(models.Model):
    name = models.CharField(max_length=255)
    manufacturer = models.ForeignKey("DeviceManufacturer", on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["manufacturer", "name"],
                name="unique_manufacturer_and_name",
            )
        ]

    def __str__(self):
        return f"{self.manufacturer} {self.name}"


class DeviceManager(models.Manager):
    def active(self):
        return self.filter(status__is_inactive=False)

    def unassigned(self):
        return self.filter(is_currently_assigned=False)

    def assigned(self):
        return self.filter(is_currently_assigned=True)

    def ready_to_assign(self):
        return self.filter(is_currently_assigned=False).filter(
            status__is_inactive=False
        )

    def get_queryset(self):
        qs = super().get_queryset()

        # Add a count of current assignments
        qs = qs.annotate(
            current_assignment_count=Count(
                F("deviceassignments"),
                filter=Q(deviceassignments__return_datetime=None),
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

        # Set is_google_linked
        qs = qs.annotate(
            is_google_linked=Max(
                Case(When(google_device__isnull=True, then=V(0)), default=V(1))
            )
        )
        return qs


class Device(models.Model):
    serial_number = models.CharField(max_length=255, unique=True)
    asset_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
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
    tags = models.ManyToManyField(DeviceTag, blank=True, related_name="devices")

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

    # If Google Device
    if device.google_device is not None:
        if instance.return_datetime is None:
            device_assignment_creation_action(person, device)
        else:
            device_turnin_action(person, device)
        # change_device_ou(device, person.type)


def device_assignment_creation_action(person, device):
    mapping_model = apps.get_model("googlesync.DeviceBuildingToGoogleOUMapping")
    mapping = mapping_model.objects.filter(
        building=device.building, person_type=person.type
    ).first()
    if (
        mapping is not None
        and mapping.organization_unit != device.google_device.organization_unit
    ):
        response = change_device_ou(
            mapping.organization_unit,
            device,
        )


def device_turnin_action(person, device):
    # Get unassigned location based on profile of person assigned
    # For now hard code it...
    response = change_device_ou(
        "/Unassigned Devices",
        device,
    )


def change_device_ou(ou, device, **kwargs):
    """Function to change a single device's OU"""
    response = call_command(
        "move_google_devices",
        ou,
        device.google_device.id,
    )
    if response == "":
        device.google_device.organization_unit = ou
        device.google_device.save()
        # Log a change
    else:
        # Log an error
        pass


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
