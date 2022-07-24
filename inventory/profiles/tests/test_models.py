from django.test import TestCase

from authentication.tests.factories import UserFactory
from .factories import ProfileFactory
from profiles.models import Profile
from timezone_field import TimeZoneField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import factory


class ProfileTest(TestCase):
    @classmethod
    @factory.django.mute_signals(post_save)
    def setUpTestData(cls):
        ProfileFactory(id=1)

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

    def test_post_save_signal(self):
        """Upon user creation, a profile should be created"""
        user = UserFactory(id=2)
        self.assertIsNotNone(user.profile.timezone)
