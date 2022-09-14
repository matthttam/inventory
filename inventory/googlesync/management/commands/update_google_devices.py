from assignments.models import DeviceAssignment
from devices.models import Device
from django.db.models import F, Q
from django.db.models import Value as V
from django.db.models.functions import Concat
from django_mysql.models import GroupConcat

from ._google_sync import GoogleSyncCommandAbstract


class Command(GoogleSyncCommandAbstract):
    help = "Updates google device data based on assignment data"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        chromeosdevices_service = self._get_chromeosdevices_service()

        devices = self.get_devices_to_update()
        patch_requests = self.get_chromeosdevices_patch_requests(
            chromeosdevices_service, devices
        )
        responses = list()
        for request in patch_requests:
            # print(request)
            responses.append(request.execute())
        # responses = self._process_batch_requests(
        #    service=chromeosdevices_service,
        #    requests=patch_requests,
        #    callback=self._patch_location_request_callback,
        # )
        self.stdout.write(self.style.SUCCESS("Done"))

    def _patch_location_request_callback(self, request_id, response, exception) -> None:
        if exception is not None:
            self.stdout.write(
                self.style.ERROR(
                    f"Failed to update google chromeos device data: {exception}"
                )
            )

    def get_chromeosdevices_patch_requests(self, service, devices: list[dict]) -> list:
        requests = list()
        for device in devices:
            body = {"annotatedLocation": device.get("correct_google_location")}
            # body = {"annotatedLocation": "test"}
            options = {
                "customerId": self.customer.get("id"),
                "projection": "FULL",
                "deviceId": device.get("google_id"),
                "body": body,
            }

            requests.append(service.patch(**options))
        return requests

    def get_devices_to_update(self) -> list[dict]:

        # Get outstanding assignments with google_devices
        # Concatinate the building and a comma list of person emails
        outstanding_devices = (
            DeviceAssignment.objects.outstanding()
            .select_related("device", "person")
            .exclude(device__google_device=None)
            .exclude(person__type__name="Staff")
            .values("device__google_device__id")
            .annotate(
                correct_google_location=Concat(
                    F("device__building__name"),
                    V(","),
                    GroupConcat(F("person__email"), order="asc"),
                )
            )
            .annotate(current_google_location=F("device__google_device__location"))
            .values(
                google_id=F("device__google_device__id"),
                correct_google_location=F("correct_google_location"),
                current_google_location=F("current_google_location"),
            )
        )
        # Get a list of all other devices and set them to Building,*
        unassigned_devices_needing_updates = (
            Device.objects.exclude(google_device=None)
            .exclude(
                google_device__id__in=outstanding_devices.values_list(
                    "google_id", flat=True
                )
            )
            .annotate(correct_google_location=Concat(F("building__name"), V(",*")))
            .annotate(current_google_location=F("google_device__location"))
            .filter(
                Q(current_google_location=None)
                | ~Q(correct_google_location=F("current_google_location"))
            )
            .values(
                google_id=F("google_device__id"),
                correct_google_location=F("correct_google_location"),
                current_google_location=F("current_google_location"),
            )
        )
        outstanding_devices_needing_updates = outstanding_devices.filter(
            Q(current_google_location=None)
            | ~Q(correct_google_location=F("current_google_location"))
        )
        return list(
            outstanding_devices_needing_updates.union(
                unassigned_devices_needing_updates
            )
        )

    def move_google_device(self, organization_unit, google_ids: list[str]):
        devices = self._get_chromeosdevices_service()

        body = {"deviceIds": google_ids}
        options = {
            "customerId": self.customer.get("id"),
            "orgUnitPath": organization_unit,
            "body": body,
        }

        request = devices.moveDevicesToOu(**options)
        response = request.execute()
        return response
