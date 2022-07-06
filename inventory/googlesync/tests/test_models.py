from django.test import TestCase
from .factories import GoogleDeviceFactory
from googlesync.models import GoogleDevice


class GoogleDeviceTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # GoogleDeviceFactory()
        pass

    def setUp(self):
        google_device = GoogleDeviceFactory()
        self.google_device = GoogleDevice.objects.get(id=google_device.id)

    def test_google_id_label(self):
        field_label = self.google_device._meta.get_field("id").verbose_name
        self.assertEqual(field_label, "id")

    def test_google_id_max_length(self):
        max_length = self.google_device._meta.get_field("id").max_length
        self.assertEqual(max_length, 255)

    def test_google_id_unique(self):
        unique = self.google_device._meta.get_field("id").unique
        self.assertTrue(unique)

    def test_google_id_required(self):
        self.assertEqual(self.google_device._meta.get_field("id").blank, False)
        self.assertEqual(self.google_device._meta.get_field("id").null, False)

    def test_google_status_label(self):
        field_label = self.google_device._meta.get_field("status").verbose_name
        self.assertEqual(field_label, "status")

    def test_google_status_max_length(self):
        max_length = self.google_device._meta.get_field("status").max_length
        self.assertEqual(max_length, 255)

    def test_google_status_optional(self):
        self.assertEqual(self.google_device._meta.get_field("status").blank, True)
        self.assertEqual(self.google_device._meta.get_field("status").null, False)

    def test_google_organization_unit_label(self):
        field_label = self.google_device._meta.get_field(
            "organization_unit"
        ).verbose_name
        self.assertEqual(field_label, "organization unit")

    def test_google_organization_unit_max_length(self):
        max_length = self.google_device._meta.get_field("organization_unit").max_length
        self.assertEqual(max_length, 255)

    def test_google_organization_unit_optional(self):
        self.assertEqual(
            self.google_device._meta.get_field("organization_unit").blank, True
        )
        self.assertEqual(
            self.google_device._meta.get_field("organization_unit").null, False
        )

    def test_google_enrollment_time_label(self):
        field_label = self.google_device._meta.get_field("enrollment_time").verbose_name
        self.assertEqual(field_label, "enrollment time")

    def test_google_enrollment_time_optional(self):
        self.assertEqual(
            self.google_device._meta.get_field("enrollment_time").blank, True
        )
        self.assertEqual(
            self.google_device._meta.get_field("enrollment_time").null, True
        )

    def test_google_last_policy_sync_label(self):
        field_label = self.google_device._meta.get_field(
            "last_policy_sync"
        ).verbose_name
        self.assertEqual(field_label, "last policy sync")

    def test_google_last_policy_sync_optional(self):
        self.assertEqual(
            self.google_device._meta.get_field("last_policy_sync").blank, True
        )
        self.assertEqual(
            self.google_device._meta.get_field("last_policy_sync").null, True
        )

    def test_google_location_label(self):
        field_label = self.google_device._meta.get_field("location").verbose_name
        self.assertEqual(field_label, "location")

    def test_google_location_max_length(self):
        max_length = self.google_device._meta.get_field("location").max_length
        self.assertEqual(max_length, 255)

    def test_google_location_optional(self):
        self.assertEqual(self.google_device._meta.get_field("location").blank, True)
        self.assertEqual(self.google_device._meta.get_field("location").null, False)

    def test_google_most_recent_user_label(self):
        field_label = self.google_device._meta.get_field(
            "most_recent_user"
        ).verbose_name
        self.assertEqual(field_label, "most recent user")

    def test_google_most_recent_user_max_length(self):
        max_length = self.google_device._meta.get_field("most_recent_user").max_length
        self.assertEqual(max_length, 255)

    def test_google_most_recent_user_optional(self):
        self.assertEqual(
            self.google_device._meta.get_field("most_recent_user").blank, True
        )
        self.assertEqual(
            self.google_device._meta.get_field("most_recent_user").null, False
        )
