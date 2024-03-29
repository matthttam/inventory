import re, operator
from functools import reduce
from django.views.generic import (
    DetailView,
    UpdateView,
    CreateView,
    DeleteView,
    FormView,
)
from django.views.generic.base import TemplateView
from django.utils import timezone
from django_datatable_serverside_mixin.views import (
    ServerSideDatatableMixin,
)
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from django.db.models.functions import Concat
from django.db.models import CharField, Value as V, Q
from django.shortcuts import redirect

from auditlog.models import LogEntry

from inventory.utils import (
    get_permitted_actions,
    get_history_table_context,
)
from inventory.views import JSONListView, JSONFormView
from people.models import Person
from devices.models import Device
from .models import DeviceAssignment
from .forms import DeviceAssignmentForm, DeviceAssignmentTurninForm


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
    extra_context = {
        "tables": {
            "assignment_list": {
                "id": "assignment_list",
                "headers": [
                    "ID",
                    "Person",
                    "Device",
                    "Assignment Date",
                    "Return Date",
                    "Actions",
                ],
            }
        },
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["permitted_actions"] = get_permitted_actions(
            self.request,
            "assignments",
            "deviceassignment",
            action_paths=[
                ("view", "detail"),
                ("change", "edit"),
                ("turnin", "turnin"),
                ("delete", "delete"),
            ],
        )
        return context


class DeviceAssignmentDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "assignments.view_deviceassignment"
    model = DeviceAssignment
    extra_context = {"tables": get_history_table_context("deviceassignment_history")}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["log_entries"] = self.object.history.all().order_by("timestamp")
        context["infobox"] = get_deviceassignment_infobox_data(context.get("object"))
        return context


class DeviceAssignmentUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "assignments.change_deviceassignment"
    model = DeviceAssignment
    fields = ["person", "device", "return_datetime"]


class DeviceAssignmentTurninView(PermissionRequiredMixin, UpdateView):
    permission_required = "assignments.turnin_deviceassignment"
    template_name = "assignments/deviceassignment_turnin_form.html"
    form_class = DeviceAssignmentTurninForm
    model = DeviceAssignment

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["infobox"] = get_deviceassignment_infobox_data(context.get("object"))
        return context

    # Don't allow turnin if already turned in
    def render_to_response(self, context, **response_kwargs):
        assignment = context.get("object")
        if assignment.return_datetime is not None:
            return redirect(reverse("assignments:detail", args=[assignment.id]))
        return super().render_to_response(context, **response_kwargs)


class DeviceAssignmentCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "assignments.add_deviceassignment"
    form_class = DeviceAssignmentForm
    template_name = "assignments/deviceassignment_form.html"


class DeviceAssignmentDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "assignments.delete_deviceassignment"
    model = DeviceAssignment
    success_url = reverse_lazy("assignments:index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["infobox"] = get_deviceassignment_infobox_data(context.get("object"))
        return context


class DeviceAssignmentQuickAssignView(PermissionRequiredMixin, TemplateView):
    permission_required = "assignments.add_deviceassignment"
    template_name = "assignments/deviceassignment_quickassign.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ajax_urls"] = {
            "people": reverse("assignments:quickassign_person_list"),
            "devices": reverse("assignments:quickassign_device_list"),
            "submit": reverse("assignments:quickassign_submit"),
        }
        return context


class QuickAssignPersonListJSONView(PermissionRequiredMixin, JSONListView):
    permission_required = "assignments.add_deviceassignment"

    def get_queryset(self):
        q = self.request.GET.get("q")
        # Remove symbols and repeated spaces
        # q = re.sub("\s+", " ", re.sub(r"[\W]", " ", q))
        people = Person.objects.all()
        if q != "":
            filter = (
                Q(internal_id__istartswith=q)
                | Q(first_name__icontains=q)
                | Q(last_name__icontains=q)
                | Q(email__istartswith=q)
            )

            search_word_list = q.replace(",", "").split(" ")
            if len(search_word_list) > 1:
                # filter |= Q(full_name__in=search_word_list)
                filter |= reduce(
                    operator.and_, (Q(full_name__icontains=x) for x in search_word_list)
                )
            people = people.filter(filter)

        people = people.values(
            "id",
            "first_name",
            "last_name",
            "internal_id",
            "is_currently_assigned",
            "email",
            "is_active",
        ).order_by("-is_active", "is_currently_assigned", "type", "last_name")
        return people


class QuickAssignDeviceListJSONView(PermissionRequiredMixin, JSONListView):
    permission_required = "assignments.add_deviceassignment"

    def get_queryset(self):
        q = self.request.GET.get("q")
        # Remove symbols and repeated spaces
        # q = re.sub("\s+", " ", re.sub(r"[\W]", " ", q))
        devices = Device.objects.all()
        if q != "":
            devices = devices.filter(
                Q(serial_number__icontains=q) | Q(asset_id__icontains=q)
            )
        devices = devices.values(
            "id", "asset_id", "serial_number", "is_active", "is_currently_assigned"
        ).order_by("-is_active", "is_currently_assigned", "asset_id", "serial_number")
        return devices


class QuickAssignSubmitView(PermissionRequiredMixin, JSONFormView):
    permission_required = "assignments.add_deviceassignment"
    form_class = DeviceAssignmentForm


def get_deviceassignment_infobox_data(deviceassignment) -> list:

    return [
        {"label": "Assignment ID :", "value": deviceassignment.id},
        {"label": "Person :", "value": deviceassignment.person},
        {"label": "Device :", "value": deviceassignment.device},
        {
            "label": "Assignment Date :",
            "date": deviceassignment.assignment_datetime,
            "value": "None",
        },
        {
            "label": "Return Date :",
            "date": deviceassignment.return_datetime,
            "value": "None",
        },
    ]
