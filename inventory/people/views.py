from django.views.generic import (
    TemplateView,
    DetailView,
    UpdateView,
    CreateView,
    DeleteView,
)
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy

from django_datatable_serverside_mixin.views import (
    ServerSideDatatableMixin,
)

from auditlog.models import LogEntry

from inventory.utils import (
    get_permitted_actions,
    get_table_context,
    get_history_table_context,
)
from inventory.aggregates import GroupConcat
from .models import Person
from .forms import PersonForm


@method_decorator(csrf_exempt, name="dispatch")
class PersonDatatableServerSideProcessingView(
    PermissionRequiredMixin, ServerSideDatatableMixin
):
    permission_required = "people.view_person"
    queryset = Person.objects.all()
    # .annotate(        building_name_list=GroupConcat("buildings__name", ", ")    )
    columns = [
        "id",
        "first_name",
        "middle_name",
        "last_name",
        "email",
        "internal_id",
        "type__name",
        "status__name",
        "primary_building__name",
    ]


class PersonListView(PermissionRequiredMixin, TemplateView):
    permission_required = "people.view_person"
    template_name = "people/person_list.html"
    extra_context = {
        "tables": {
            "person_list": {
                "id": "person_list",
                "headers": [
                    "ID",
                    "First Name",
                    "Last Name",
                    "Email",
                    "Internal ID",
                    "Type",
                    "Status",
                    "Building",
                    "Actions",
                ],
            }
        },
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["permitted_actions"] = get_permitted_actions(
            self.request, "people", "person"
        )
        return context


class PersonDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "people.view_person"
    model = Person
    extra_context = {"tables": get_history_table_context("person_history")}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["log_entries"] = LogEntry.objects.filter(
            object_id=self.object.id
        ).order_by("timestamp")
        return context


class PersonUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "people.change_person"
    model = Person
    fields = [
        "internal_id",
        "first_name",
        "middle_name",
        "last_name",
        "email",
        "type",
        "status",
    ]


class PersonCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "people.add_person"
    form_class = PersonForm
    template_name = "people/person_form.html"


class PersonDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "people.delete_person"
    model = Person
    success_url = reverse_lazy("people:index")
