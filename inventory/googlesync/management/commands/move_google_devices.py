from ._google_sync import GoogleSyncCommandAbstract


class Command(GoogleSyncCommandAbstract):
    help = "Moves a google device's OU"

    def add_arguments(self, parser):
        parser.add_argument(
            "organization_unit", nargs="?", help="Path or ID of Organization Unit"
        )
        parser.add_argument("google_ids", nargs="*", help="List of google ids")

    def handle(self, *args, **options):

        organization_unit = options.get("organization_unit")
        google_ids = options.get("google_ids")
        self.move_google_device(organization_unit, google_ids)
        self.stdout.write(self.style.SUCCESS("Done"))

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
