from django.core.management import call_command


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
