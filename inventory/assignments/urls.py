from django.urls import path, include
from .views import *
from .views import DeviceAssignmentListView, DeviceAssignmentDetailView, DeviceAssignmentCreateView, DeviceAssignmentUpdateView

app_name = 'assignments'
urlpatterns = [
    path('', DeviceAssignmentListView.as_view(), name='index'),
    path('<int:pk>/', DeviceAssignmentDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', DeviceAssignmentUpdateView.as_view(), name='edit'),
    path('new/', DeviceAssignmentCreateView.as_view(), name='new'),
]
