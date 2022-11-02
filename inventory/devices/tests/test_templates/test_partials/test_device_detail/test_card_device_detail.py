from django.test import SimpleTestCase
from django.template import Context, Template
from bs4 import BeautifulSoup
from devices.tests.factories import DeviceFactory


class CardDeviceDetailButtonsPermissionTest(SimpleTestCase):
    def setUp(self):
        device = DeviceFactory.stub(id=1)
        self.context = Context(
            {
                "device": device,
                "perms": {
                    "devices": {
                        "view_device": True,
                        "change_device": False,
                        "delete_device": False,
                    }
                },
            }
        )
        self.template = Template(
            "{% include  'devices/partials/device_detail/card_device_detail.html'%}"
        )
        self.list_link_selector = 'a[href="/devices/"]'
        self.edit_link_selector = 'a[href="/devices/1/edit/"]'
        self.delete_link_selector = 'a[href="/devices/1/delete/"]'

    def test_view_permissions(self):
        rendered = self.template.render(self.context)
        self.soup = BeautifulSoup(rendered, "html.parser")
        print(self.soup)
        list_link = self.soup.select_one(self.list_link_selector)
        edit_link = self.soup.select_one(self.edit_link_selector)
        delete_link = self.soup.select_one(self.delete_link_selector)
        self.assertIsNotNone(list_link)
        self.assertIsNone(edit_link)
        self.assertIsNone(delete_link)

    def test_edit_permissions(self):
        self.context["perms"]["devices"]["change_device"] = True
        rendered = self.template.render(self.context)
        self.soup = BeautifulSoup(rendered, "html.parser")
        list_link = self.soup.select_one(self.list_link_selector)
        edit_link = self.soup.select_one(self.edit_link_selector)
        delete_link = self.soup.select_one(self.delete_link_selector)
        self.assertIsNotNone(list_link)
        self.assertIsNotNone(edit_link)
        self.assertIsNone(delete_link)

    def test_delete_permissions(self):
        self.context["perms"]["devices"]["delete_device"] = True
        rendered = self.template.render(self.context)
        self.soup = BeautifulSoup(rendered, "html.parser")
        list_link = self.soup.select_one(self.list_link_selector)
        edit_link = self.soup.select_one(self.edit_link_selector)
        delete_link = self.soup.select_one(self.delete_link_selector)
        self.assertIsNotNone(list_link)
        self.assertIsNone(edit_link)
        self.assertIsNotNone(delete_link)
