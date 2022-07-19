from django.shortcuts import render
from .models import Device
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from .forms import DeviceForm
from inventory.views.django_serverside_datatable.views import ServerSideDatatableMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import PermissionRequiredMixin


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


class DeviceUpdateView(UpdateView):
    model = Device
    fields = ["serial_number", "asset_id", "device_model", "notes"]


class DeviceCreateView(CreateView):
    form_class = DeviceForm
    template_name = "devices/device_form.html"
