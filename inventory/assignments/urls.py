from django.urls import path, include
from .views import *
from .views import (
    DeviceAssignmentListView,
    DeviceAssignmentDetailView,
    DeviceAssignmentCreateView,
    DeviceAssignmentUpdateView,
    DeviceAssignmentDatatableServerSideProcessingView,
)

app_name = "assignments"
urlpatterns = [
    path("", DeviceAssignmentListView.as_view(), name="index"),
    path(
        "dt/",
        DeviceAssignmentDatatableServerSideProcessingView.as_view(),
        name="dt_index",
    ),
    path("<int:pk>/", DeviceAssignmentDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", DeviceAssignmentUpdateView.as_view(), name="edit"),
    path("new/", DeviceAssignmentCreateView.as_view(), name="new"),
]
