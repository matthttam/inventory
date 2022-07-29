from django.views.generic import (
    TemplateView,
    DetailView,
    UpdateView,
    CreateView,
    DeleteView,
)
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy

from django_datatable_serverside_mixin.views import (
    ServerSideDatatableMixin,
)

from auditlog.models import LogEntry

from inventory.utils import (
    get_permitted_actions,
    get_table_context,
    get_history_table_context,
)
from .forms import DeviceForm
from .models import Device


@method_decorator(csrf_exempt, name="dispatch")
class DeviceDatatableServerSideProcessingView(
    PermissionRequiredMixin, ServerSideDatatableMixin
):
    permission_required = "devices.view_device"
    queryset = Device.objects.all()
    columns = [
        "id",
        "asset_id",
        "serial_number",
    ]


class DeviceListView(PermissionRequiredMixin, TemplateView):
    permission_required = "devices.view_device"
    template_name = "devices/device_list.html"
    extra_context = {
        "tables": {
            "device_list": {
                "id": "device_list",
                "headers": ["ID", "Asset ID", "Serial Number", "Actions"],
            }
        },
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["permitted_actions"] = get_permitted_actions(
            self.request, "devices", "device"
        )
        return context


class DeviceDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "devices.view_device"
    model = Device
    extra_context = {"tables": get_history_table_context("device_history")}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["log_entries"] = LogEntry.objects.filter(
            object_id=self.object.id
        ).order_by("timestamp")
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
