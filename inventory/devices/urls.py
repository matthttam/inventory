from django.urls import path, include
from .views import *
from .views import DeviceListView, DeviceDetailView, DeviceCreateView, DeviceUpdateView

app_name = 'devices'
urlpatterns = [
    path('', DeviceListView.as_view(), name='index'),
    path('<int:pk>/', DeviceDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', DeviceUpdateView.as_view(), name='edit'),
    path('new/', DeviceCreateView.as_view(), name='new'),
]
