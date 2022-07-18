from django.http import JsonResponse
from django.shortcuts import render
from .models import Person, PersonType
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from .forms import PersonForm
from django.views.generic.base import View
import json
from django.core.serializers import serialize
from django.db.models import CharField, Value as V, F, Subquery
from django.db.models.functions import Concat
from locations.models import Building
from inventory.aggregates import GroupConcat


class DatatableServerSideProcessingView(View):
    def get(self, *args, **kwargs):
        people = Person.objects.values(
            "id",
            "first_name",
            "middle_name",
            "last_name",
            "email",
            "internal_id",
            "type__name",
            "status__name",
        ).annotate(building_name_list=GroupConcat("buildings__name", ", "))
        breakpoint()
        return JsonResponse({"data": list(people)})


class PersonListView(ListView):
    model = Person

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # context.person.building_list = "a,b,c"
        return context


class PersonDetailView(DetailView):
    model = Person


class PersonUpdateView(UpdateView):
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
