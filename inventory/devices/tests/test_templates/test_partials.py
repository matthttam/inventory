from devices.tests.factories import DeviceFactory, DeviceModelFactory, DeviceStatusFactory, DeviceTagFactory
from assignments.tests.factories import DeviceAssignmentFactory, DeviceAssignmentWithReturnDatetimeFactory
from django.template import Context, Template
from django.template.loader import render_to_string
from django.test import SimpleTestCase
from googlesync.tests.factories import GoogleDeviceFactory
from locations.tests.factories import BuildingFactory, RoomFactory
from bs4 import BeautifulSoup
from sekizai.context import SekizaiContext


class DetailCardDeviceDetailTest(SimpleTestCase):
    template = "devices/partials/detail/card_device_detail.html"

    def test_template(self):
        templates = [
            "partials/card.html",
            "devices/partials/device_tag_list.html",
        ]
        for template in templates:
            with self.assertTemplateUsed(template):
                render_to_string(self.template)

    def test_has_device_id(self):
        context = {"device": DeviceFactory.stub(id=100)}
        render = render_to_string(self.template, context=context)
        self.assertInHTML("<li>Device ID : 100</li>", render)

    def test_has_device_asset_id(self):
        context = {"device": DeviceFactory.stub(asset_id="ASSET_1234ABCD")}
        render = render_to_string(self.template, context=context)
        self.assertInHTML("<li>Asset Tag : ASSET_1234ABCD</li>", render)

    def test_has_device_serial_number(self):
        context = {"device": DeviceFactory.stub(serial_number="SERIAL_ABCD1234")}
        render = render_to_string(self.template, context=context)
        self.assertInHTML("<li>Serial Number : SERIAL_ABCD1234</li>", render)

    def test_has_device_status(self):
        status = DeviceStatusFactory.build()
        context = {"device": DeviceFactory.stub(status=status)}
        render = render_to_string(self.template, context=context)
        self.assertInHTML(f"<li>Status : {status}</li>", render)

    def test_has_device_model(self):
        device_model = DeviceModelFactory.build()
        context = {"device": DeviceFactory.stub(device_model=device_model)}
        render = render_to_string(self.template, context=context)
        self.assertInHTML(f"<li>Model : {device_model}</li>", render)

    def test_has_device_building(self):
        building = BuildingFactory.build()
        context = {"device": DeviceFactory.stub(building=building)}
        render = render_to_string(self.template, context=context)
        self.assertInHTML(f"<li>Building : {building}</li>", render)

    def test_has_device_room(self):
        room = RoomFactory.build()
        context = {"device": DeviceFactory.stub(room=room)}
        render = render_to_string(self.template, context=context)
        self.assertInHTML(f"<li>Room : {room}</li>", render)

    def test_has_device_tags(self):
        tags = DeviceTagFactory.build_batch(size=3)
        context = {"device": DeviceFactory.stub(room=tags)}
        render = render_to_string(self.template, context=context)
        tag_render = render_to_string("devices/partials/device_tag_list.html", context=context)
        self.assertInHTML(f"<li>Tags : {tag_render}</li>", render)

    def test_has_notes(self):
        context = {"device": DeviceFactory.stub(notes="NOTES_ABCD1234")}
        render = render_to_string(self.template, context=context)
        self.assertInHTML("<li>Notes : NOTES_ABCD1234</li>", render)


class DetailCardDeviceDetailButtonPermissionTest(SimpleTestCase):
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
        self.template = Template("{% include  'devices/partials/detail/card_device_detail.html'%}")
        self.list_link_selector = 'a[href="/devices/"]'
        self.edit_link_selector = 'a[href="/devices/1/edit/"]'
        self.delete_link_selector = 'a[href="/devices/1/delete/"]'

    def test_view_permissions(self):
        rendered = self.template.render(self.context)
        self.soup = BeautifulSoup(rendered, "html.parser")
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


class DetailCardDeviceHistoryTest(SimpleTestCase):
    template = "devices/partials/detail/card_device_history.html"

    def test_template(self):
        templates = [
            "partials/card.html",
            "partials/table.html",
        ]
        for template in templates:
            with self.assertTemplateUsed(template):
                render_to_string(self.template, context=SekizaiContext().flatten())


class DetailCardDeviceAssignmentHistoryTest(SimpleTestCase):
    template = "devices/partials/detail/card_deviceassignment_history.html"

    def test_template(self):
        templates = [
            "partials/card.html",
            "assignments/partials/deviceassignment_detail/table_deviceassignment.html",
        ]
        for template in templates:
            with self.assertTemplateUsed(template):
                render_to_string(self.template)


class DetailCardGoogleDeviceDetailTest(SimpleTestCase):
    template = "devices/partials/detail/card_google_device_detail.html"

    def setUp(self) -> None:
        self.google_device = GoogleDeviceFactory.build()
        self.device = DeviceFactory.stub(google_device=self.google_device, is_google_linked=True)
        self.context = {"device": self.device}
        self.render = render_to_string(self.template, context=self.context)
        return super().setUp()

    def test_template(self):
        templates = [
            "partials/card.html",
        ]
        for template in templates:
            with self.assertTemplateUsed(template):
                render_to_string(self.template)

    def test_google_device_id(self):
        self.assertInHTML(f"<li>Google ID : {self.google_device.id}</li>", self.render)

    def test_google_device_asset_tag(self):
        self.assertInHTML(f"<li>Asset Tag : {self.google_device.annotated_asset_id}</li>", self.render)

    def test_google_device_serial_number(self):
        self.assertInHTML(f"<li>Serial Number : {self.google_device.serial_number}</li>", self.render)

    def test_google_device_status(self):
        self.assertInHTML(f"<li>Status : {self.google_device.status}</li>", self.render)

    def test_google_device_device_model(self):
        self.assertInHTML(f"<li>Model : {self.google_device.device_model}</li>", self.render)

    def test_google_device_most_recent_user(self):
        self.assertInHTML(f"<li>Most Recent User : {self.google_device.most_recent_user}</li>", self.render)

    def test_google_device_ou(self):
        self.assertInHTML(f"<li>OU : {self.google_device.organization_unit}</li>", self.render)

    def test_google_device_location(self):
        self.assertInHTML(f"<li>Location : {self.google_device.location}</li>", self.render)

    def test_google_device_enrollment_time(self):
        rendered_datetime = Template("{{datetime}}").render(Context({"datetime": self.google_device.enrollment_time}))
        self.assertInHTML(f"<li>Enrollment Time : {rendered_datetime}</li>", self.render)

    def test_google_device_last_policy_sync(self):
        rendered_datetime = Template("{{datetime}}").render(Context({"datetime": self.google_device.last_policy_sync}))
        self.assertInHTML(f"<li>Last Policy Sync : {rendered_datetime}</li>", self.render)

    def test_google_device_missing(self):
        device = DeviceFactory.stub(google_device=None, is_google_linked=False)
        context = {"device": device}
        render = render_to_string(self.template, context=context)
        self.assertInHTML(f'<div class="card-text p-4">Not Linked to a Google Device</div>', render)


class DetailCardOutstandingAssignmentsTest(SimpleTestCase):
    template = "devices/partials/detail/card_outstanding_assignments.html"

    def test_template_assigned_device(self):
        templates = [
            "partials/card.html",
            "assignments/partials/deviceassignment_detail/table_deviceassignment.html",
        ]

        device = DeviceFactory.build()
        device.is_currently_assigned = True
        device.outstanding_assignments = [
            DeviceAssignmentFactory.build(id=1, device=device),
        ]

        context = {"device": device}

        for template in templates:
            with self.assertTemplateUsed(template):
                render_to_string(self.template, context=context)

    def test_template_unassigned_device(self):
        templates = [
            "assignments/partials/deviceassignment_detail/table_deviceassignment.html",
        ]
        device_assignment = DeviceAssignmentWithReturnDatetimeFactory.build()
        context = {"device": device_assignment.device}

        for template in templates:
            with self.assertTemplateNotUsed(template):
                render_to_string(self.template, context=context)


class DetailInnerNavTest(SimpleTestCase):
    template = "devices/partials/detail/inner_nav.html"

    def setUp(self):
        self.device_detail_tab = 'a[href="#device-detail-tab"]'
        self.device_history_tab = 'a[href="#device-history-tab"]'
        self.assignment_history_tab = 'a[href="#assignment-history-tab"]'
        self.rendered = render_to_string(self.template, context=SekizaiContext().flatten())
        self.soup = BeautifulSoup(self.rendered, "html.parser")

    def test_template(self):
        templates = [
            "partials/inner_nav.html",
        ]

        for template in templates:
            with self.assertTemplateUsed(template):
                render_to_string(self.template, context=SekizaiContext().flatten())

    def test_detail_tab(self):
        device_detail_tab = self.soup.select_one(self.device_detail_tab)
        self.assertIsNotNone(device_detail_tab)
        self.assertEqual(list(device_detail_tab.stripped_strings)[0], "Details")
        self.assertEqual(device_detail_tab.attrs["data-bs-toggle"], "tab")
        self.assertEqual(device_detail_tab.attrs["data-bs-target"], "#device-detail")

    def test_history_tab(self):
        device_history_tab = self.soup.select_one(self.device_history_tab)
        self.assertIsNotNone(device_history_tab)
        self.assertEqual(list(device_history_tab.stripped_strings)[0], "History")
        self.assertEqual(device_history_tab.attrs["data-bs-toggle"], "tab")
        self.assertEqual(device_history_tab.attrs["data-bs-target"], "#device-history")

    def test_assignment_history_tab(self):
        assignment_history_tab = self.soup.select_one(self.assignment_history_tab)
        self.assertIsNotNone(assignment_history_tab)
        self.assertEqual(list(assignment_history_tab.stripped_strings)[0], "Assignment History")
        self.assertEqual(assignment_history_tab.attrs["data-bs-toggle"], "tab")
        self.assertEqual(assignment_history_tab.attrs["data-bs-target"], "#assignment-history")


class DetailStickyHeaderTest(SimpleTestCase):
    template = "devices/partials/detail/sticky_header.html"

    def test_template(self):
        templates = [
            "partials/detail/sticky_header.html",
            "devices/partials/device_tag_icons.html",
        ]
        tag = DeviceTagFactory.build()
        context = SekizaiContext(
            {
                "device": {
                    "tags": {
                        "all": [
                            tag,
                        ]
                    },
                    "is_currently_assigned": True,
                }
            }
        )
        for template in templates:
            with self.assertTemplateUsed(template):
                render_to_string(self.template, context=context.flatten())

    def test_template_assigned_device(self):
        tag = DeviceTagFactory.build()
        context = SekizaiContext(
            {
                "device": {
                    "tags": {
                        "all": [
                            tag,
                        ]
                    },
                    "is_currently_assigned": True,
                }
            }
        )
        self.assertInHTML(
            '<span class="text-success">Assigned</span>',
            render_to_string(self.template, context=context.flatten()),
        )

    def test_template_unassigned_device(self):
        tag = DeviceTagFactory.build()
        context = SekizaiContext(
            {
                "device": {
                    "tags": {
                        "all": [
                            tag,
                        ]
                    },
                    "is_currently_assigned": False,
                }
            }
        )

        self.assertInHTML(
            '<span class="text-secondary">Unassigned</span>',
            render_to_string(self.template, context=context.flatten()),
        )


class DetailTabDeviceDetailTest(SimpleTestCase):
    template = "devices/partials/detail/tab_device_detail.html"

    def test_template(self):
        templates = [
            "devices/partials/detail/card_device_detail.html",
            "devices/partials/detail/card_outstanding_assignments.html",
            "devices/partials/detail/card_google_device_detail.html",
        ]

        for template in templates:
            with self.assertTemplateUsed(template):
                render_to_string(self.template)


class DetailTabDeviceHistoryTest(SimpleTestCase):
    template = "devices/partials/detail/tab_device_history.html"

    def test_template(self):
        templates = [
            "devices/partials/detail/card_device_history.html",
        ]

        for template in templates:
            with self.assertTemplateUsed(template):
                render_to_string(self.template, context=SekizaiContext().flatten())


class DetailTabDeviceAssignmentHistoryTest(SimpleTestCase):
    template = "devices/partials/detail/tab_deviceassignment_history.html"

    def test_template(self):
        templates = [
            "devices/partials/detail/card_deviceassignment_history.html",
        ]

        for template in templates:
            with self.assertTemplateUsed(template):
                render_to_string(self.template)


class ListTableRowButtonsTest(SimpleTestCase):
    template = "devices/partials/list/table_row_buttons.html"

    def test_template(self):
        templates = [
            "partials/action_button_group.html",
        ]

        for template in templates:
            with self.assertTemplateUsed(template):
                render_to_string(self.template)


class ListTableRowButtonsPermissionTest(SimpleTestCase):
    def setUp(self):
        device = DeviceFactory.build(id=1)
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
        self.template = Template("{% include  'devices/partials/list/table_row_buttons.html'%}")
        self.view_link_selector = 'a[href="/devices/1/"]'
        self.edit_link_selector = 'a[href="/devices/1/edit/"]'
        self.delete_link_selector = 'a[href="/devices/1/delete/"]'

    def test_view_permissions(self):
        rendered = self.template.render(self.context)
        self.soup = BeautifulSoup(rendered, "html.parser")
        view_link = self.soup.select_one(self.view_link_selector)
        edit_link = self.soup.select_one(self.edit_link_selector)
        delete_link = self.soup.select_one(self.delete_link_selector)
        self.assertIsNotNone(view_link)
        self.assertIsNone(edit_link)
        self.assertIsNone(delete_link)

    def test_edit_permissions(self):
        self.context["perms"]["devices"]["change_device"] = True
        rendered = self.template.render(self.context)
        self.soup = BeautifulSoup(rendered, "html.parser")
        view_link = self.soup.select_one(self.view_link_selector)
        edit_link = self.soup.select_one(self.edit_link_selector)
        delete_link = self.soup.select_one(self.delete_link_selector)
        self.assertIsNotNone(view_link)
        self.assertIsNotNone(edit_link)
        self.assertIsNone(delete_link)

    def test_delete_permissions(self):
        self.context["perms"]["devices"]["delete_device"] = True
        rendered = self.template.render(self.context)
        self.soup = BeautifulSoup(rendered, "html.parser")
        view_link = self.soup.select_one(self.view_link_selector)
        edit_link = self.soup.select_one(self.edit_link_selector)
        delete_link = self.soup.select_one(self.delete_link_selector)
        self.assertIsNotNone(view_link)
        self.assertIsNone(edit_link)
        self.assertIsNotNone(delete_link)


class DeviceTagIcons(SimpleTestCase):
    template = "devices/partials/device_tag_icons.html"

    def test_no_tags(self):
        tag = DeviceTagFactory.build()
        context = {"device": {"tags": {"all": []}}}
        templates = [
            "partials/tag_icon.html",
        ]
        for template in templates:
            with self.assertTemplateNotUsed(template):
                render_to_string(self.template, context=context)

    def test_with_tags(self):
        tag = DeviceTagFactory.build()
        context = {
            "device": {
                "tags": {
                    "all": [
                        tag,
                    ]
                }
            }
        }
        templates = [
            "partials/tag_icon.html",
        ]
        for template in templates:
            with self.assertTemplateUsed(template):
                render_to_string(self.template, context=context)


class DeviceTagList(SimpleTestCase):
    template = "devices/partials/device_tag_list.html"

    def test_tag_name(self):
        tag = DeviceTagFactory.build()
        context = {
            "device": {
                "tags": {
                    "all": [
                        tag,
                    ]
                }
            }
        }
        render = render_to_string(self.template, context=context)
        self.assertInHTML(
            f'<span class="badge rounded-pill text-bg-primary d-inline-block ms-2">{tag.name}</span>', render
        )

    def test_multiple_tag_names(self):
        tags = DeviceTagFactory.build_batch(size=3)
        context = {"device": {"tags": {"all": tags}}}
        render = render_to_string(self.template, context=context)
        for tag in tags:
            self.assertInHTML(
                f'<span class="badge rounded-pill text-bg-primary d-inline-block ms-2">{tag.name}</span>', render
            )
