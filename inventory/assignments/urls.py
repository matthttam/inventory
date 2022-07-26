from django.urls import path, include
from .views import (
    DeviceAssignmentListView,
    DeviceAssignmentDetailView,
    DeviceAssignmentCreateView,
    DeviceAssignmentUpdateView,
    DeviceAssignmentDeleteView,
    DeviceAssignmentQuickAssignView,
    DeviceAssignmentDatatableServerSideProcessingView,
    quick_assign_user_list_view,
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
    path("quickassign/", DeviceAssignmentQuickAssignView.as_view(), name="quickassign"),
    path("<int:pk>/delete/", DeviceAssignmentDeleteView.as_view(), name="delete"),
    path(
        "quickassign/ajax/users/",
        quick_assign_user_list_view,
        name="quick_assign_user_list",
    ),
]
