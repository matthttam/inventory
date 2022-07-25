from django.urls import path, include
from .views import ProfileUpdateView, ProfileView

app_name = "profile"
urlpatterns = [
    path("", ProfileView.as_view(), name="profile"),
    path("edit/", ProfileUpdateView.as_view(), name="edit"),
]
