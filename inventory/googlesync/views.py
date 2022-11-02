from inspect import Attribute
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, ListView
from .forms import (
    GoogleConfigForm,
    GoogleServiceAccountConfig,
    GoogleServiceAccountConfigForm,
    GooglePersonMappingForm,
)
from .models import (
    GoogleConfig,
    GoogleServiceAccountConfig,
    GooglePersonMapping,
    GoogleDeviceMapping,
)
from utils.mixins import SuperuserRequiredMixin


class GoogleConfigCreateUpdateView(SuperuserRequiredMixin, UpdateView):
    model = GoogleConfig
    form_class = GoogleConfigForm
    template_name = "googlesync/googleconfig_form.html"

    def get_object(self, queryset=None):
        return self.model.objects.first()
        # try:
        #    return super().get_object(queryset)
        # except AttributeError:
        #    return None

    # fields = ['client_id', 'project_id', 'client_secret']


class GoogleServiceAccountConfigCreateUpdateView(SuperuserRequiredMixin, UpdateView):
    model = GoogleServiceAccountConfig
    form_class = GoogleServiceAccountConfigForm
    template_name = "googlesync/googleconfig_form.html"

    def get_object(self, queryset=None):
        return self.model.objects.first()


class GooglePersonMappingListView(SuperuserRequiredMixin, ListView):
    model = GooglePersonMapping


class GoogleDeviceMappingListView(SuperuserRequiredMixin, ListView):
    model = GoogleDeviceMapping


class GooglePersonMappingUpdateView(SuperuserRequiredMixin, UpdateView):
    model = GooglePersonMapping
    fields = ["from_field", "to_field", "matching_priority"]


class GoogleDeviceMappingUpdateView(SuperuserRequiredMixin, UpdateView):
    model = GoogleDeviceMapping
    fields = ["from_field", "to_field", "matching_priority"]
