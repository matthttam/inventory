from django.shortcuts import render
from .models import DeviceAssignment
from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
    CreateView,
    DeleteView,
)
from django.views.generic.base import TemplateView
from .forms import DeviceAssignmentForm
from django.utils import timezone
from django_datatable_serverside_mixin.views import (
    ServerSideDatatableMixin,
)
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.db.models.functions import Concat
from django.db.models import CharField, Value as V


@method_decorator(csrf_exempt, name="dispatch")
class DeviceAssignmentDatatableServerSideProcessingView(
    PermissionRequiredMixin, ServerSideDatatableMixin
):
    permission_required = "assignments.view_deviceassignment"
    queryset = DeviceAssignment.objects.all().annotate(
        person_name=Concat(
            "person__first_name", V(" "), "person__last_name", output_field=CharField()
        )
    )
    columns = [
        "id",
        "person_name",
        "device__asset_id",
        "assignment_datetime",
        "return_datetime",
    ]


class DeviceAssignmentListView(PermissionRequiredMixin, TemplateView):
    permission_required = "assignments.view_deviceassignment"
    template_name = "assignments/deviceassignment_list.html"


class DeviceAssignmentDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "assignments.view_deviceassignment"
    model = DeviceAssignment


class DeviceAssignmentUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "assignments.change_deviceassignment"
    model = DeviceAssignment
    fields = ["assignment_datetime", "return_datetime"]


class DeviceAssignmentCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "assignments.add_deviceassignment"
    form_class = DeviceAssignmentForm
    template_name = "assignments/deviceassignment_form.html"

    def form_valid(self, form):
        form.instance.assignment_datetime = timezone.now()
        return super().form_valid(form)


class DeviceAssignmentDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "assignments.delete_deviceassignment"
    model = DeviceAssignment
    success_url = reverse_lazy("assignments:index")
