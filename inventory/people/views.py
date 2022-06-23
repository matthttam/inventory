from django.shortcuts import render
from .models import Person, PersonType
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from .forms import PersonForm


class PersonListView(ListView):
    model = Person
    #context_object_name = 'devices'


class PersonDetailView(DetailView):
    model = Person


class PersonUpdateView(UpdateView):
    model = Person
    fields = ['internal_id', 'first_name',
              'middle_name', 'last_name', 'email', 'type', 'status']


class PersonCreateView(CreateView):
    form_class = PersonForm
    template_name = "people/person_form.html"
