from django.test import TestCase
from .factories import ProfileFactory
from profiles.models import Profile
from timezone_field import TimeZoneField
from django.contrib.auth.models import User


class ProfileTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        ProfileFactory()

    def setUp(self):
        self.profile = Profile.objects.get(id=1)

    def test_custom_timezone_type(self):
        timezone = self.profile._meta.get_field("timezone")
        self.assertIsInstance(timezone, TimeZoneField)
        print(timezone.__class__)

    def test_user_foreign_key(self):
        user = self.profile._meta.get_field("user")
        self.assertEqual(user)

    def test_user_foreign_key(self):
        self.assertEqual(self.profile._meta.get_field("user").related_model, User)
