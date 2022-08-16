from ._google_sync import GoogleSyncCommandAbstract
from devices.models import Device
from django.db.models.functions import Concat
from django.db.models import CharField, Value as V, Q, F, Case, When, Prefetch
from django_mysql.models import GroupConcat
from assignments.models import DeviceAssignment
from googleapiclient.http import BatchHttpRequest

import pdb


class Command(GoogleSyncCommandAbstract):
    help = "Updates google device data based on assignment data"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        chromeosdevices = self._get_chromeosdevices_service()

        devices = self.get_devices_to_update()
        patch_requests = self.get_chromeosdevices_patch_requests(
            chromeosdevices, devices
        )
        responses = self._process_batch_requests(
            service=chromeosdevices,
            requests=patch_requests,
            callback=self._patch_location_request_callback,
        )
        self.stdout.write(self.style.SUCCESS("Done"))

    def _process_batch_requests(
        self, service, requests: list, callback=None, start=0, max=1000
    ) -> list:
        responses = list()

        while start < len(requests):
            print(dir(service))
            # batch = service.new_batch_http_request(callback=callback)
            batch = BatchHttpRequest(
                callback=callback,
                batch_uri="https://www.googleapis.com/batch/admin/v1",
            )
            for request in requests[start:max]:
                batch.add(request)
            responses.append(batch.execute())
            start = max
            max *= 2
        return responses

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
            .annotate(
                correct_google_location=Concat(
                    F("device__building__name"),
                    V(","),
                    GroupConcat(F("person__email"), order="asc"),
                )
            )
            .annotate(current_google_location=F("device__google_device__location"))
            .filter(
                Q(current_google_location=None)
                | ~Q(correct_google_location=F("current_google_location"))
            )
            .values(
                google_id=F("device__google_device__id"),
                correct_google_location=F("correct_google_location"),
                current_google_location=F("current_google_location"),
            )
        )
        # Get a list of all other devices and set them to Building,*
        unassigned_devices = (
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
        return list(outstanding_devices.union(unassigned_devices))

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
