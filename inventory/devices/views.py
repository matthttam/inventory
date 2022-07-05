from django.shortcuts import render
from .models import Device
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from .forms import DeviceForm


class DeviceListView(ListView):
    model = Device
    # context_object_name = 'devices'


class DeviceDetailView(DetailView):
    model = Device


class DeviceUpdateView(UpdateView):
    model = Device
    fields = ["serial_number", "asset_id", "device_model", "notes"]


class DeviceCreateView(CreateView):
    form_class = DeviceForm
    template_name = "devices/device_form.html"
