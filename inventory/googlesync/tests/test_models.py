from django.test import TestCase
from .factories import GoogleDeviceFactory


class GoogleDeviceTest(TestCase):
    def test_factory(self):
        google_device = GoogleDeviceFactory()
