from assignments.models import DeviceAssignment
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Case, Max, Prefetch
from django.db.models import Value as V
from django.db.models import When
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    TemplateView,
    UpdateView,
)
from django_datatable_serverside_mixin.views import ServerSideDataTablesMixin
from inventory.utils import get_history_table_context

from .forms import DeviceForm
from .models import Device


@method_decorator(csrf_exempt, name="dispatch")
class DeviceDatatableServerSideProcessingView(
    PermissionRequiredMixin, ServerSideDataTablesMixin
):
    def data_callback(self, data: list[dict]) -> list[dict]:
        for row in data:
            row["actions"] = render_to_string(
                "devices/partials/device_list/table_row_buttons.html",
                context={"device": row},
                request=self.request,
            )

        return super().data_callback(data)

    permission_required = "devices.view_device"
    queryset = (
        Device.objects.all()
        .select_related(
            "status",
            "device_model",
            "device_model__manufacturer",
            "building",
            "google_device",
            "room",
        )
        .annotate(
            is_google_linked=Max(
                Case(When(google_device__isnull=True, then=V(0)), default=V(1))
            )
        )
    )
    columns = [
        "id",
        "is_currently_assigned",
        "current_assignment_count",
        "asset_id",
        "serial_number",
        "status__name",
        "device_model__manufacturer__name",
        "device_model__name",
        "building__name",
        "is_google_linked",
        "google_device__organization_unit",
        "google_device__most_recent_user",
    ]


class DeviceListView(PermissionRequiredMixin, TemplateView):
    permission_required = "devices.view_device"
    template_name = "devices/device_list.html"
    extra_context = {
        "tables": {
            "device_list": {
                "id": "device_list",
                "headers": [
                    "ID",
                    "Assigned",
                    "Assignment Count",
                    "Asset ID",
                    "Serial Number",
                    "Status",
                    "Manufacturer",
                    "Model",
                    "Building",
                    "G Link",
                    "G OU",
                    "G Most Recent User",
                    "Actions",
                ],
            }
        },
    }


class DeviceDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "devices.view_device"
    # model = Device
    extra_context = {"tables": get_history_table_context("device_history")}
    queryset = Device.objects.prefetch_related(
        Prefetch(
            "deviceassignments",
            queryset=DeviceAssignment.objects.filter(return_datetime=None),
            to_attr="outstanding_assignments",
        )
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["log_entries"] = (
            context.get("object").history.all().order_by("timestamp")
        )
        context["infobox"] = get_device_infobox_data(context.get("object"))
        return context


class DeviceUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "devices.change_device"
    model = Device
    form_class = DeviceForm


class DeviceCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "devices.add_device"
    form_class = DeviceForm
    template_name = "devices/device_form.html"


class DeviceDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "devices.delete_device"
    model = Device
    success_url = reverse_lazy("devices:index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["infobox"] = get_device_infobox_data(context.get("object"))
        return context


def get_device_infobox_data(device) -> list:

    return [
        {"label": "Device ID :", "value": device.id},
        {"label": "Serial Number :", "value": device.serial_number},
        {"label": "Asset Tag :", "value": device.asset_id},
        {"label": "Status :", "value": device.status},
        {"label": "Model :", "value": device.device_model},
        {"label": "Building :", "value": device.building},
        {"label": "Room :", "value": device.room},
    ]
