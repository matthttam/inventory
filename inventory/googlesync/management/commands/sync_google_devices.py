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

from ._google_sync import GoogleSyncCommand
from devices.models import DeviceManufacturer, DeviceModel, DeviceStatus


class Command(GoogleSyncCommand):
    help = "Syncs google devices to inventory devices."

    def add_arguments(self, parser):
        parser.add_argument("profiles", nargs="+")

    def handle(self, *args, **options):
        profile_names = options.get("profiles")

        # Get each sync profile based on profile names passed
        self.sync_profiles = []
        for profile_name in profile_names:
            self.sync_profiles.append(self._get_device_sync_profile(profile_name))

        # Loop over each sync profile and sync people
        for sync_profile in self.sync_profiles:
            self.stdout.write(
                self.style.NOTICE(f"Starting devices sync: {sync_profile.name}")
            )
            self.sync_google_devices(sync_profile)

        self.stdout.write(self.style.SUCCESS("Done"))

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
            orgUnitPath=org_unit_path or None,
            query=query or None,
        )

        google_device_records = []
        while request is not None:
            response = request.execute()
            google_devices = response.get("chromeosdevices")
            if not google_devices:
                self.stdout.write(
                    self.style.WARNING(
                        f"No users found with google query: {sync_profile.google_query!r}"
                    )
                )
                return None
            google_device_records.extend(google_devices)
            request = devices.list_next(request, response)
            # request = None
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

        # active_device_status = DeviceStatus.objects.filter(is_inactive=False).first()
        inactive_device_status = DeviceStatus.objects.filter(is_inactive=True).first()
        found_record_ids = []
        records_to_update = []
        records_to_create = []
        records_to_skip = []

        unique_field_values = {}
        # unique_fields = [
        #    x.name for x in Device._meta.fields if x.unique == True and x.name != "id"
        # ]
        unique_fields = [
            {"name": x.name, "blank": x.blank}
            for x in GoogleDevice._meta.fields
            if x.unique == True and x.name != "id"
        ]

        for unique_field in unique_fields:
            unique_field_values[unique_field["name"]] = []

        for device_record in device_records:

            # Build a query to search through each ID specified
            query = Q()

            # Use lookup ids in order of matching_priority
            lookup_ids = [
                x.to_field
                for x in GoogleDeviceMapping.objects.exclude(
                    matching_priority=None
                ).order_by("matching_priority")
            ]
            for id_field in lookup_ids:
                query.add(Q(**{id_field: getattr(device_record, id_field)}), Q.OR)
            id = getattr(GoogleDevice.objects.filter(query).first(), "id", None)
            if id:
                found_record_ids.append(id)
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
            excluded_fields = ["id'"]
            fields = [
                x.name
                for x in GoogleDevice._meta.fields
                if (x.name not in excluded_fields)
            ]
            GoogleDevice.objects.bulk_update(records_to_update, fields=fields)

            # Inactivate Records Not Found
            # missing_records = (
            #    GoogleDevice.objects.exclude(google_id__isnull=True)
            #    .filter(google_sync_profile=sync_profile)
            #    .difference(Device.objects.filter(id__in=found_record_ids))
            # )

            # with transaction.atomic():
            #     for missing_record in missing_records:
            #         missing_record.status = inactive_device_status
            #         missing_record.save()
            #         self.stdout.write(
            #             self.style.WARNING(
            #                 f"Device not found. Setting to Inactive: {missing_record}"
            #             )
            #         )
            # Device.objects.update(, fields=)
        print(records_to_create[0].__dict__)
        # Create New Records
        if records_to_create:
            GoogleDevice.objects.bulk_create(records_to_create)

    def convert_google_devices_to_google_devices(
        self, sync_profile: GoogleDeviceSyncProfile, google_users: list
    ) -> list[GoogleDevice]:
        device_records = []
        for google_user in google_users:
            device = self.convert_google_device_to_google_device(
                sync_profile, google_user
            )
            if not device:
                continue
            device_records.append(device)
        return device_records

    def convert_google_device_to_google_device(
        self, sync_profile: GoogleDeviceSyncProfile, google_device: dict
    ) -> GoogleDevice:

        device_dictionary = self._map_dictionary(sync_profile, google_device)

        # mappings = GoogleDeviceMapping.objects.filter(sync_profile=sync_profile)

        # for mapping in mappings:
        #    try:
        #        device[mapping.to_field] = self._extract_from_dictionary(
        #            user, mapping.from_field.split(".")
        #        )
        #    except KeyError:
        #        device[mapping.to_field] = None
        #
        #    # Use translations to convert one value to another
        #    translations = GoogleDeviceTranslation.objects.filter(
        #        google_device_mapping=mapping
        #    )
        #
        #    for translation in translations:
        #        if str(device[mapping.to_field]) == translation.translate_from:
        #            device[mapping.to_field] = translation.translate_to

        # Map Device status
        # device_status_object = DeviceStatus.objects.filter(
        #    name=device["status"]
        # ).first()
        # if not device_status_object:
        #    self.stdout.write(
        #        self.style.ERROR(
        #            f"Device status {device['status']} not a valid option. Either create this device status or map this to a valid device status."
        #        )
        #    )
        #    return None
        # device["status"] = device_status_object

        # Map Device model
        # if not device["device_model"]:
        #    self.stdout.write(
        #        self.style.ERROR(
        #            f"Required field device model blank for google device {device!r}."
        #        )
        #    )
        #    return None
        # (
        #    device_model_object,
        #    device_model_object_created,
        # ) = DeviceModel.objects.get_or_create(
        #    name=device["device_model"],
        #    defaults={
        #        "manufacturer": DeviceManufacturer.objects.filter(
        #            name=device["device_model"].split()[0]
        #        ).first()
        #    },
        # )

        # if device_model_object_created:
        #    self.stdout.write(
        #        self.style.SUCCESS(
        #            f"Device model {device_model_object.name!r} created with manufacturer {device_model_object.manufacturer!r}."
        #        )
        #    )
        # device_model_object = DeviceModel.objects.filter(
        #    name=device["device_model"]
        # ).first()
        # if not device_model_object:
        #    self.stdout.write(
        #        self.style.ERROR(
        #            f"Device model {device['device_model']} not a valid option. Either create this device model or map this to a valid device model."
        #        )
        #    )
        #    return None
        # device["device_model"] = device_model_object

        # Set sync_profile
        # device["google_sync_profile"] = sync_profile
        # Create a Device object

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
