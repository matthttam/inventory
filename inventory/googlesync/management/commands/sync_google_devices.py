from googlesync.exceptions import SyncProfileNotFound

from googlesync.models import (
    GoogleDeviceMapping,
    GoogleDeviceTranslation,
    GoogleDeviceSyncProfile,
    GoogleDevice,
)

from django.core.exceptions import ValidationError
from django.db.models import Q
from django.db import transaction
from googlesync.models import GoogleCustomSchema, GooglePersonSyncProfile
from ._google_sync import GoogleSyncCommandAbstract
from devices.models import DeviceManufacturer, DeviceModel, DeviceStatus


class Command(GoogleSyncCommandAbstract):
    help = "Syncs google devices to inventory devices."

    def add_arguments(self, parser):
        # parser.add_argument("profiles", nargs="+")
        subparsers = parser.add_subparsers(
            title="Command Options", help="", dest="command"
        )
        ### init command ###
        init_subparser = subparsers.add_parser(
            "init",
            help="Initialize google device sync by pulling chrome os schema data from google.",
        )
        init_subparser.add_argument(
            "--force",
            action="store_true",
            help="Used to reinitialize the google device schema.",
        )
        ### profiles command ###
        sync_subparser = subparsers.add_parser(
            "sync", help="Used to initiate a sync of all profiles."
        )
        sync_subparser.add_argument(
            "profiles", nargs="*", help="List of device profiles to sync."
        )

    def handle(self, *args, **options):
        command = options.get("command")
        if command == "init":
            force = options.get("force")
            self._initilaize_device_sync(force=force)
        elif command == "sync":
            profile_names = options.get("profiles")
            if profile_names:
                # Get each sync profile based on profile names passed
                self.sync_profiles = []
                for profile_name in profile_names:
                    self.sync_profiles.append(
                        self._get_device_sync_profile(profile_name)
                    )
            else:
                self.sync_profiles = list(GoogleDeviceSyncProfile.objects.all())
            self._sync_google_device_profiles(self.sync_profiles)
        else:
            return False
        self.stdout.write(self.style.SUCCESS("Done"))

    @transaction.atomic
    def _initilaize_device_sync(self, force):
        """Gets all Device related schema information and saves it to the database."""
        self.stdout.write(self.style.SUCCESS(f"Starting device sync initialization."))
        if self.google_config.get("device_initialized"):
            if not force:
                self.stdout.write(
                    self.style.ERROR(
                        f"Google Device Sync already initialized. Use --force to override."
                    )
                )
                return
            else:
                self.stdout.write(self.style.WARNING(f"Forcing reinitialization."))
        # Delete any schemas already stored
        self._delete_default_schemas("ChromeOsDevice")
        self._initialize_default_schema("ChromeOsDevice")

        # Set acocunt as initialized
        google_config = self._get_google_config()
        google_config.person_initialized = True
        google_config.save()

    def _sync_google_device_profiles(
        self, sync_profiles: list[GoogleDeviceSyncProfile]
    ):
        for sync_profile in self.sync_profiles:
            self._sync_google_device_profile(sync_profile)

    def _sync_google_device_profile(self, sync_profile: GoogleDeviceSyncProfile):
        self.stdout.write(
            self.style.SUCCESS(f"Starting devices sync: {sync_profile.name}")
        )
        self.sync_google_devices(sync_profile)

    def _get_device_sync_profile(self, profile_name):
        try:
            sync_profile = GoogleDeviceSyncProfile.objects.get(name=profile_name)
        except GoogleDeviceSyncProfile.DoesNotExist:
            raise SyncProfileNotFound(profile_name=profile_name)
        return sync_profile

    def _get_google_records(self, query, org_unit_path) -> list:
        devices = self._get_chromeosdevices_service()
        request = devices.list(
            customerId=self.customer.get("id"),
            projection="FULL",
            query=query or None,
            orgUnitPath=org_unit_path or None,
        )

        google_device_records = []
        while request is not None:
            response = request.execute()
            google_devices = response.get("chromeosdevices")
            if not google_devices:
                self.stdout.write(
                    self.style.WARNING(
                        f"No devices found with google query: {query!r} within org path: {org_unit_path!r}"
                    )
                )
                return None
            google_device_records.extend(google_devices)
            request = devices.list_next(request, response)
            # request = None  # !!!!!
        return google_device_records

    def sync_google_devices(self, sync_profile):
        google_devices = self._get_google_records(
            query=sync_profile.google_query,
            org_unit_path=sync_profile.google_org_unit_path,
        )
        device_records = self.convert_google_devices_to_google_devices(
            sync_profile, google_devices
        )

        self.stdout.write(
            self.style.SUCCESS(f"Total Number of device records: {len(device_records)}")
        )

        # inactive_device_status = DeviceStatus.objects.filter(is_inactive=True).first()
        records_to_update = []
        records_to_create = []
        records_to_skip = []

        unique_field_values = {}
        unique_fields = [
            {"name": x.name, "blank": x.blank}
            for x in GoogleDevice._meta.fields
            if x.unique == True and x.name != "id"
        ]

        for unique_field in unique_fields:
            unique_field_values[unique_field["name"]] = []

        for device_record in device_records:
            id = GoogleDevice.objects.filter(id=device_record.id).only("id").first().id
            if id:
                device_record.id = id
                records_to_update.append(device_record)
            else:

                # if device_record.status != inactive_device_status:
                # Valid Uniqueness for bulk creation
                is_valid = True
                for unique_field in unique_fields:
                    device_record_value = getattr(device_record, unique_field["name"])
                    if device_record_value in unique_field_values[unique_field["name"]]:
                        is_valid = False
                        self.stdout.write(
                            self.style.ERROR(
                                f"Uniqueness constraint for {unique_field['name']!r} failed when creating device: {device_record}"
                            )
                        )
                    else:
                        if device_record_value is not None:
                            unique_field_values[unique_field["name"]].append(
                                device_record_value
                            )
                if is_valid:
                    records_to_create.append(device_record)
                # else:
                #    records_to_skip.append(device_record)

        print(f"Number of device records to update: {len(records_to_update)}")
        print(f"Number of device records to create: {len(records_to_create)}")
        print(f"Number of device records to skip: {len(records_to_skip)}")

        # Update found records
        if records_to_update:
            excluded_fields = ["id"]
            fields = [
                x.name
                for x in GoogleDevice._meta.fields
                if (x.name not in excluded_fields)
            ]
            print(fields)
            GoogleDevice.objects.bulk_update(records_to_update, fields=fields)

        # Create New Records
        if records_to_create:
            GoogleDevice.objects.bulk_create(records_to_create)

    def convert_google_devices_to_google_devices(
        self, sync_profile: GoogleDeviceSyncProfile, google_devices: list
    ) -> list[GoogleDevice]:
        device_records = []
        for google_device in google_devices:
            device = self.convert_google_device_to_google_device(
                sync_profile, google_device
            )
            if not device:
                continue
            device_records.append(device)
        return device_records

    def convert_google_device_to_google_device(
        self, sync_profile: GoogleDeviceSyncProfile, google_device: dict
    ) -> GoogleDevice:

        device_dictionary = self._map_dictionary(sync_profile, google_device)

        device = GoogleDevice(**device_dictionary)
        try:
            device.clean_fields()
        except ValidationError as e:
            self.stdout.write(
                self.style.WARNING(
                    f"Validation Error when validating google device: {device_dictionary}"
                )
            )
            self.stdout.write(self.style.WARNING(f"{e.message_dict}"))
            return None
        return device
