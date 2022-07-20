from django.shortcuts import render
from .models import DeviceAssignment
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.views.generic.base import TemplateView
from .forms import DeviceAssignmentForm
from django.utils import timezone
from django_datatable_serverside_mixin.views import (
    ServerSideDatatableMixin,
)
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import PermissionRequiredMixin


@method_decorator(csrf_exempt, name="dispatch")
class DeviceAssignmentDatatableServerSideProcessingView(
    PermissionRequiredMixin, ServerSideDatatableMixin
):
    permission_required = "deviceassignments.view_deviceassignment"
    queryset = DeviceAssignment.objects.all()
    # .annotate( building_name_list=GroupConcat("buildings__name", ", ") )
    columns = [
        "id",
        "person__first_name",
        "device__asset_id",
        "assignment_datetime",
        "return_datetime",
    ]


class DeviceAssignmentListView(PermissionRequiredMixin, TemplateView):
    permission_required = "deviceassignments.view_deviceassignment"
    template_name = "assignments/deviceassignment_list.html"


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
