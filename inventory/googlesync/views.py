from inspect import Attribute
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, ListView
from .forms import GoogleConfigForm, GoogleServiceAccountConfig, GoogleServiceAccountConfigForm, GooglePersonMappingForm
from .models import GoogleConfig, GoogleServiceAccountConfig, GooglePersonMapping


class GoogleConfigCreateUpdateView(UpdateView):
    model = GoogleConfig
    form_class = GoogleConfigForm
    template_name = 'googlesync/googleconfig_form.html'

    def get_object(self, queryset=None):
        return self.model.objects.first()
        # try:
        #    return super().get_object(queryset)
        # except AttributeError:
        #    return None

    #fields = ['client_id', 'project_id', 'client_secret']


class GoogleServiceAccountConfigCreateUpdateView(UpdateView):
    model = GoogleServiceAccountConfig
    form_class = GoogleServiceAccountConfigForm
    template_name = 'googlesync/googleconfig_form.html'

    def get_object(self, queryset=None):
        return self.model.objects.first()


class GooglePersonMappingListView(ListView):
    model = GooglePersonMapping


class GooglePersonMappingCreateUpdateView(UpdateView):
    model = GooglePersonMapping
    form_class = GooglePersonMappingForm
    template_name = 'googlesync/googleconfig_form.html'

    def get_object(self, queryset=None):
        return self.model.objects.first()
