from django.test import SimpleTestCase, TestCase
from django.template import Context, Template
from bs4 import BeautifulSoup
import copy
from devices.tests.factories import DeviceFactory
from django.urls import reverse
from zoneinfo import ZoneInfo
from authentication.tests.factories import SuperuserUserFactory
from datetime import datetime

list_link_selector = 'a[href="/devices/"]'
update_link_selector = 'a[href="/devices/1/edit/"]'
delete_link_selector = 'a[href="/devices/1/delete/"]'

default_context = Context(
    {
        "TIME_ZONE": "America/Chicago",
        "device": {
            "id": 1,
            "serial_number": "Test Serial",
            "asset_id": "Test Asset ID",
            "status": "Test Status",
            "device_model": "Test Model",
            "building": "Test Building",
            "room": "Test Room",
        },
        "perms": {
            "devices": {
                "view_device": True,
                "delete_device": True,
                "change_device": True,
            }
        },
    }
)

default_template = Template("{% include  'devices/partials/device_infobox.html'%}")
