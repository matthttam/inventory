from django.core.management.base import BaseCommand
from django.test import TestCase
from parameterized import parameterized
from django.core.management import call_command

from googlesync.management.commands._google_sync import GoogleSyncCommandAbstract
from googlesync.management.commands.sync_google_devices import (
    Command as GoogleDevicesSyncCommand,
)
from googlesync.management.commands.link_google_devices import (
    Command as GoogleDevicesLinkCommand,
)
from googlesync.management.commands.sync_google_people import (
    Command as GooglePeopleSyncCommand,
)
from googlesync.exceptions import ConfigNotFound, SyncProfileNotFound

from googlesync.models import (
    GooglePersonSyncProfile,
    GoogleServiceAccountConfig,
    GoogleDeviceSyncProfile,
    GoogleDevice,
)
from googlesync.tests.factories import (
    GoogleConfigFactory,
    GoogleDeviceSyncProfileFactory,
    GooglePersonMappingFactory,
    GooglePersonSyncProfileFactory,
    GooglePersonTranslationFactory,
    GoogleServiceAccountConfigFactory,
    GoogleDeviceFactory,
)
from unittest.mock import MagicMock, call, patch, Mock
from io import StringIO
from django.forms import model_to_dict
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import Resource
import pytest

from people.tests.factories import PersonFactory, PersonStatusFactory, PersonTypeFactory
from people.models import Person


class LinkGoogleDevicesTest(TestCase):
    def test_subclass(self):
        self.assertTrue(issubclass(GoogleDevicesLinkCommand, BaseCommand))

    def test_help(self):
        self.assertEqual(
            GoogleDevicesLinkCommand.help,
            "Associate imported device to their Google device counterpart.",
        )
