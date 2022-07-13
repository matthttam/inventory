from django.core.management.base import BaseCommand
from googlesync.models import GoogleDevice, GoogleDeviceSyncProfile
from devices.models import Device
from googlesync.exceptions import SyncProfileNotFound
from django.db.models import Q


class Command(BaseCommand):
    help = "Syncs google devices to inventory devices."

    def add_arguments(self, parser):
        parser.add_argument("profile", nargs="?")

    def handle(self, *args, **options):
        profile_name = options.get("profile")
        try:
            self.sync_profile = GoogleDeviceSyncProfile.objects.get(name=profile_name)
        except GoogleDeviceSyncProfile.DoesNotExist:
            raise SyncProfileNotFound(profile_name=profile_name)

        self._link_google_devices()

    def _link_google_devices(self):
        google_devices = GoogleDevice.objects.all()
        if not google_devices:
            self.stdout.write(
                self.style.NOTICE(
                    f"No Google Devices have been synced yet to link to devices."
                )
            )
        devices = Device.objects.filter(google_device=None)
        if not devices:
            self.stdout.write(self.style.NOTICE(f"No Unlinked Devices exist."))
        for device in devices:
            # Build a query to search through each ID specified
            query = Q()

            # Use lookup ids in order of matching_priority
            lookup_ids = [
                x.from_field
                for x in self.sync_profile.link_mappings.exclude(
                    matching_priority=None
                ).order_by("matching_priority")
            ]
            link_mapping_ids = self.sync_profile.link_mappings.exclude(
                matching_priority=None
            ).order_by("matching_priority")

            for link_mapping in link_mapping_ids:
                query.add(
                    Q(
                        **{
                            link_mapping.from_field: getattr(
                                device, link_mapping.to_field
                            )
                        }
                    ),
                    Q.OR,
                )
            # id = getattr(GoogleDevice.objects.filter(query).first(), "id", None)
            found_google_device = GoogleDevice.objects.filter(query).first()

            if found_google_device:
                print(f"Found matching device: {found_google_device} for {device}")
                device.google_device = found_google_device
                device.save()
            else:
                continue
            # for id_field in lookup_ids:
            #    query.add(Q(**{id_field: getattr(device_record, id_field)}), Q.OR)
            # id = getattr(GoogleDevice.objects.filter(query).first(), "id", None)
