from django.urls import path, include
from .views import *
from .views import (
    GoogleConfigCreateUpdateView,
    GoogleServiceAccountConfigCreateUpdateView,
    GooglePersonMapping,
)

app_name = "googlesync"
urlpatterns = [
    path("config/", GoogleConfigCreateUpdateView.as_view(), name="config"),
    path(
        "serviceaccount/",
        GoogleServiceAccountConfigCreateUpdateView.as_view(),
        name="service_account_config",
    ),
    path(
        "personmapping/<int:pk>/edit/",
        GooglePersonMappingUpdateView.as_view(),
        name="person_mapping",
    ),
    path(
        "devicemapping/<int:pk>/edit/",
        GoogleDeviceMappingUpdateView.as_view(),
        name="device_mapping",
    ),
]
