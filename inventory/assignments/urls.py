from django.urls import path, include
from .views import (
    DeviceAssignmentListView,
    DeviceAssignmentDetailView,
    DeviceAssignmentCreateView,
    DeviceAssignmentUpdateView,
    DeviceAssignmentDeleteView,
    DeviceAssignmentQuickAssignView,
    DeviceAssignmentDatatableServerSideProcessingView,
    QuickAssignPersonListJSONView,
    QuickAssignDeviceListJSONView,
    QuickAssignSubmitView,
    DeviceAssignmentTurninView,
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
    path("<int:pk>/turnin/", DeviceAssignmentTurninView.as_view(), name="turnin"),
    path("new/", DeviceAssignmentCreateView.as_view(), name="new"),
    path("quickassign/", DeviceAssignmentQuickAssignView.as_view(), name="quickassign"),
    path("<int:pk>/delete/", DeviceAssignmentDeleteView.as_view(), name="delete"),
    path(
        "quickassign/ajax/people/",
        QuickAssignPersonListJSONView.as_view(),
        name="quickassign_person_list",
    ),
    path(
        "quickassign/ajax/devices/",
        QuickAssignDeviceListJSONView.as_view(),
        name="quickassign_device_list",
    ),
    path(
        "quickassign/ajax/submit/",
        QuickAssignSubmitView.as_view(),
        name="quickassign_submit",
    ),
]
