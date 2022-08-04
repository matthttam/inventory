from django.shortcuts import render
from profiles.models import Profile
from django.views.generic import UpdateView, DetailView
from django.urls import reverse


class ProfileView(DetailView):
    model = Profile

    def get_object(self, queryset=None):
        return Profile.objects.get(user_id=self.request.user.id)

    # def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    context.object = Profile.objects.get(user_id=self.request.user.id)
    #    return context


class ProfileUpdateView(UpdateView):
    model = Profile

    def get_object(self, queryset=None):
        return Profile.objects.get(user_id=self.request.user.id)

    fields = [
        "timezone",
    ]
