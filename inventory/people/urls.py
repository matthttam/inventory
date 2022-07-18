from django.urls import path, include
from .views import *

# , PersonCreateView, PersonUpdateView
from .views import PersonListView, PersonDetailView, DatatableServerSideProcessingView

app_name = "people"
urlpatterns = [
    path("", PersonListView.as_view(), name="index"),
    path("dt/", DatatableServerSideProcessingView.as_view(), name="dt"),
    path("<int:pk>/", PersonDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", PersonUpdateView.as_view(), name="edit"),
    path("new/", PersonCreateView.as_view(), name="new"),
]
