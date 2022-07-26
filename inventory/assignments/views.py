from django.views import View
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
from django.db.models import CharField, Value as V
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import permission_required
from django.db.models import F, Count, Q, When, Value, Case

from auditlog.models import LogEntry

from people.models import Person
from devices.models import Device
from .models import DeviceAssignment
from .forms import DeviceAssignmentForm, QuickAssignmentForm


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        temp_id = 12345
        placeholder = "__id_placeholder__"
        context["actions"] = {
            "view": {
                "allowed": self.request.user.has_perm(
                    "assignments.view_deviceassignment"
                ),
                "path": reverse("assignments:detail", args=[temp_id]).replace(
                    str(temp_id), placeholder
                ),
            },
            "change": {
                "allowed": self.request.user.has_perm(
                    "assignments.change_deviceassignment"
                ),
                "path": reverse("assignments:edit", args=[temp_id]).replace(
                    str(temp_id), placeholder
                ),
            },
            "delete": {
                "allowed": self.request.user.has_perm(
                    "assignments.delete_deviceassignment"
                ),
                "path": reverse("assignments:delete", args=[temp_id]).replace(
                    str(temp_id), placeholder
                ),
            },
        }
        return context


class DeviceAssignmentDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "assignments.view_deviceassignment"
    model = DeviceAssignment

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["log_entries"] = LogEntry.objects.filter(
            object_id=self.object.id
        ).order_by("timestamp")
        return context


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


class DeviceAssignmentQuickAssignView(PermissionRequiredMixin, TemplateView):
    permission_required = "assignments.add_deviceassignment"
    template_name = "assignments/deviceassignment_quick_assign.html"


@permission_required("assignments.add_deviceassignment")
@require_http_methods(["GET"])
def quick_assign_user_list_view(request):
    q = request.GET.get("q")
    people = Person.objects.all()
    if q:
        people = people.filter(
            Q(internal_id__exact=q)
            | Q(first_name__icontains=q)
            | Q(last_name__icontains=q)
            | Q(last_name__icontains=q)
            | Q(email__istartswith=q)
        )
    people = people.values(
        "id",
        "first_name",
        "last_name",
        "internal_id",
        "has_outstanding_assignment",
        "email",
        "is_active",
    ).order_by("type", "last_name")

    result = [
        {
            "text": f"{person.get('last_name')}, {person.get('first_name')} - {person.get('internal_id')}",
            "id": person.get("id"),
            "internal_id": person.get("internal_id"),
            "is_active": person.get("is_active"),
            "has_outstanding_assignment": person.get("has_outstanding_assignment"),
        }
        for person in people
    ]
    return JsonResponse({"results": result})
