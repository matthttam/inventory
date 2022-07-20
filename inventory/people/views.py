from .models import Person
from django.views.generic import DetailView, UpdateView, CreateView
from django.views.generic.base import TemplateView
from .forms import PersonForm
from inventory.aggregates import GroupConcat
from django_datatable_serverside_mixin.views import (
    ServerSideDatatableMixin,
)
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import PermissionRequiredMixin


@method_decorator(csrf_exempt, name="dispatch")
class PersonDatatableServerSideProcessingView(
    PermissionRequiredMixin, ServerSideDatatableMixin
):
    permission_required = "people.view_person"
    queryset = Person.objects.all().annotate(
        building_name_list=GroupConcat("buildings__name", ", ")
    )
    columns = [
        "id",
        "first_name",
        "middle_name",
        "last_name",
        "email",
        "internal_id",
        "type__name",
        "status__name",
        "building_name_list",
    ]


class PersonListView(PermissionRequiredMixin, TemplateView):
    permission_required = "people.view_person"
    template_name = "people/person_list.html"


class PersonDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "people.view_person"
    model = Person


class PersonUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "people.update_person"
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


class PersonCreateView(CreateView):
    form_class = PersonForm
    template_name = "people/person_form.html"
