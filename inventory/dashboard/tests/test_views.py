from django.test import TestCase
from django.urls import reverse


class DeviceIndexViewTest(TestCase):
    def test_index_view(self):
        response = self.client.get(reverse("dashboard:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/dashboard.html")
        self.assertTemplateUsed(response, "dashboard/dashboard_nav.html")
        self.assertTemplateUsed(response, "base.html")
