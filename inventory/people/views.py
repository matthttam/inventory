from django.contrib.auth.mixins import PermissionRequiredMixin
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    TemplateView,
    UpdateView,
)
from django_datatable_serverside_mixin.views import ServerSideDataTablesMixin
from inventory.utils import get_history_table_context

from .forms import PersonForm
from .models import Person


@method_decorator(csrf_exempt, name="dispatch")
class PersonDatatableServerSideProcessingView(
    PermissionRequiredMixin, ServerSideDataTablesMixin
):
    def data_callback(self, data: list[dict]) -> list[dict]:
        for row in data:
            row["actions"] = render_to_string(
                "people/partials/person_list/table_row_buttons.html",
                context={"person": row},
                request=self.request,
            )

        return super().data_callback(data)

    permission_required = "people.view_person"
    queryset = Person.objects.all().select_related("type", "status", "primary_building")
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
        "outstanding_assignment_count",
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
                    "Assignment Count",
                    "Actions",
                ],
            }
        },
    }


class PersonDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "people.view_person"
    model = Person
    extra_context = {"tables": get_history_table_context("person_history")}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["log_entries"] = self.object.history.all().order_by("timestamp")
        context["infobox"] = get_person_infobox_data(context.get("object"))
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["infobox"] = get_person_infobox_data(context.get("object"))
        return context


def get_person_infobox_data(person) -> list:

    return [
        {"label": "Person ID :", "value": person.id},
        {"label": "First name :", "value": person.first_name},
        {"label": "Last name :", "value": person.last_name},
        {"label": "Email :", "value": person.email},
        {"label": "Primary Building :", "value": person.primary_building},
        {"label": "Internal ID :", "value": person.internal_id},
        {"label": "Type :", "value": person.type},
        {"label": "Status :", "value": person.status},
    ]
