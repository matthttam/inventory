from django.urls import path

from .views import (
    DeviceListView,
    DeviceDetailView,
    DeviceCreateView,
    DeviceUpdateView,
    DeviceDeleteView,
    DeviceDatatableServerSideProcessingView,
)

app_name = "devices"
urlpatterns = [
    path("", DeviceListView.as_view(), name="index"),
    path("dt/", DeviceDatatableServerSideProcessingView.as_view(), name="dt_index"),
    path("<int:pk>/", DeviceDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", DeviceUpdateView.as_view(), name="edit"),
    path("new/", DeviceCreateView.as_view(), name="new"),
    path("<int:pk>/delete/", DeviceDeleteView.as_view(), name="delete"),
]
