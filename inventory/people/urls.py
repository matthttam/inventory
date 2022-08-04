from django.urls import path

from .views import (
    PersonListView,
    PersonDetailView,
    PersonCreateView,
    PersonUpdateView,
    PersonDeleteView,
    PersonDatatableServerSideProcessingView,
)

app_name = "people"
urlpatterns = [
    path("", PersonListView.as_view(), name="index"),
    path("dt/", PersonDatatableServerSideProcessingView.as_view(), name="dt_index"),
    path("<int:pk>/", PersonDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", PersonUpdateView.as_view(), name="edit"),
    path("new/", PersonCreateView.as_view(), name="new"),
    path("<int:pk>/delete/", PersonDeleteView.as_view(), name="delete"),
]
