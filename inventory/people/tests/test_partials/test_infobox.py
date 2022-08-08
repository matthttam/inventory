import copy

from bs4 import BeautifulSoup
from django.template import Context, Template
from django.test import SimpleTestCase

list_link_selector = 'a[href="/people/"]'
update_link_selector = 'a[href="/people/1/edit/"]'
delete_link_selector = 'a[href="/people/1/delete/"]'

default_context = Context(
    {
        "TIME_ZONE": "America/Chicago",
        "person": {
            "id": 1,
            "first_name": "Test First Name",
            "last_name": "Test Last Name",
            "email": "Test Email",
            "primary_building": "Test Primary Building",
            "internal_id": "Test Internal ID",
            "type": "Test Type",
            "status": "Test Status",
        },
        "perms": {
            "people": {
                "view_person": True,
                "delete_person": True,
                "change_person": True,
            }
        },
    }
)

default_template = Template("{% include  'people/partials/person_infobox.html'%}")
