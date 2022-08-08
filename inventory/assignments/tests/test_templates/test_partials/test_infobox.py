from django.test import SimpleTestCase, TestCase
from django.template import Context, Template
from bs4 import BeautifulSoup
import copy
from assignments.tests.factories import DeviceAssignmentFactory
from django.urls import reverse
from zoneinfo import ZoneInfo
from authentication.tests.factories import SuperuserUserFactory
from datetime import datetime

list_link_selector = 'a[href="/assignments/"]'
update_link_selector = 'a[href="/assignments/1/edit/"]'
delete_link_selector = 'a[href="/assignments/1/delete/"]'

default_context = Context(
    {
        "TIME_ZONE": "America/Chicago",
        "deviceassignment": {
            "id": 1,
            "person": "Test Person",
            "device": "Test Device",
            "assignment_datetime": datetime(2022, 7, 1, 2, 0, 0, 0),
            "return_datetime": datetime(2022, 7, 31, 2, 0, 0, 0),
        },
        "perms": {
            "assignments": {
                "view_deviceassignment": True,
                "delete_deviceassignment": True,
                "change_deviceassignment": True,
            }
        },
    }
)

default_template = Template(
    "{% include  'assignments/partials/deviceassignment_infobox.html'%}"
)
