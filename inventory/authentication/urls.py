from django.contrib import admin
from django.urls import path, include
from dashboard import views

app_name = "authentication"
urlpatterns = [
    path("", include("django.contrib.auth.urls")),
]
