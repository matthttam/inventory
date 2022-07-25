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

from inventory.aggregates import GroupConcat
from .models import Person
from .forms import PersonForm


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
