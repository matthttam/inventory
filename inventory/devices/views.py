from django.shortcuts import render
from .models import Device
from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
    CreateView,
    DeleteView,
)
from .forms import DeviceForm
from django_datatable_serverside_mixin.views import (
    ServerSideDatatableMixin,
)
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse, reverse_lazy


@method_decorator(csrf_exempt, name="dispatch")
class DeviceDatatableServerSideProcessingView(
    PermissionRequiredMixin, ServerSideDatatableMixin
):
    permission_required = "devices.view_device"
    queryset = Device.objects.all()
    columns = [
        "id",
        "serial_number",
        "asset_id",
    ]


class DeviceListView(PermissionRequiredMixin, ListView):
    permission_required = "devices.view_device"
    model = Device


class DeviceDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "devices.view_device"
    model = Device


class DeviceUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "devices.change_device"
    model = Device
    fields = ["serial_number", "asset_id", "device_model", "notes"]


class DeviceCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "devices.add_device"
    form_class = DeviceForm
    template_name = "devices/device_form.html"


class DeviceDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "devices.delete_device"
    model = Device
    success_url = reverse_lazy("devices:index")
