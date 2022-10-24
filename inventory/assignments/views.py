import operator
from functools import reduce

from devices.models import Device
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import CharField, Q
from django.db.models import Value as V
from django.db.models.functions import Concat
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django.views.generic.base import TemplateView
from django_datatable_serverside_mixin.views import ServerSideDataTablesMixin
from inventory.utils import get_history_table_context
from inventory.views import JSONFormView, JSONListView
from people.models import Person

from .forms import DeviceAssignmentForm, DeviceAssignmentTurninForm
from .models import DeviceAssignment


@method_decorator(csrf_exempt, name="dispatch")
class DeviceAssignmentDatatableServerSideProcessingView(
    PermissionRequiredMixin, ServerSideDataTablesMixin
):
    def data_callback(self, data: list[dict]) -> list[dict]:
        for row in data:
            row["actions"] = render_to_string(
                "assignments/partials/deviceassignment_list/table_row_buttons.html",
                context={"deviceassignment": row},
                request=self.request,
            )

        return super().data_callback(data)

    permission_required = "assignments.view_deviceassignment"
    queryset = (
        DeviceAssignment.objects.all()
        .select_related("person", "device")
        .annotate(
            device_str=Concat(
                "device__asset_id",
                V(" ("),
                "device__serial_number",
                V(")"),
                output_field=CharField(),
            )
        )
        .annotate(
            person_name=Concat(
                "person__first_name",
                V(" "),
                "person__last_name",
                output_field=CharField(),
            )
        )
    )
    columns = [
        "id",
        "person__internal_id",
        "person__type__name",
        "person_name",
        "person__first_name",
        "person__last_name",
        "device_str",
        "device__asset_id",
        "device__serial_number",
        "device__device_model__name",
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
                    "Person Internal ID",
                    "Person",
                    "Person First Name",
                    "Person Last Name",
                    "Person Type",
                    "Device",
                    "Device Asset",
                    "Device Serial",
                    "Device Model",
                    "Assignment Date",
                    "Return Date",
                    '<div class="text-center">Action</div>',
                ],
            }
        },
    }


class DeviceAssignmentDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "assignments.view_deviceassignment"
    model = DeviceAssignment
    extra_context = {"tables": get_history_table_context("deviceassignment_history")}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["log_entries"] = (
            context.get("object").history.all().order_by("timestamp")
        )
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
