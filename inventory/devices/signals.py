from django.apps import apps
from django.dispatch import receiver
from django.db.models.signals import post_save

from googlesync.utils import change_device_ou


@receiver(post_save, sender="assignments.DeviceAssignment")
def device_assignment_actions(sender, instance, update_fields, **kwargs):
    """When assigned to a person the device building should be the person's primary building"""
    person = instance.person
    device = instance.device

    if (
        person.primary_building is not None
        and person.primary_building != device.building
    ):
        device.building = person.primary_building
        device.save()

    # If Google Device
    if device.google_device is not None:
        if instance.return_datetime is None:
            device_assignment_creation_action(person, device)
        else:
            device_turnin_action(person, device)


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
