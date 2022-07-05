from django.shortcuts import render
from .models import DeviceAssignment, DeviceAccessoryAssignment
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from .forms import DeviceAssignmentForm
from django.utils import timezone


class DeviceAssignmentListView(ListView):
    model = DeviceAssignment
    # context_object_name = 'devices'


class DeviceAssignmentDetailView(DetailView):
    model = DeviceAssignment


class DeviceAssignmentUpdateView(UpdateView):
    model = DeviceAssignment
    fields = ["assignment_datetime", "return_datetime"]


class DeviceAssignmentCreateView(CreateView):
    form_class = DeviceAssignmentForm
    template_name = "assignments/deviceassignment_form.html"

    def form_valid(self, form):
        form.instance.assignment_datetime = timezone.now()
        return super().form_valid(form)
