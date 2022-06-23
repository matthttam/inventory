from django.urls import path, include
from .views import *
# , PersonCreateView, PersonUpdateView
from .views import PersonListView, PersonDetailView

app_name = 'people'
urlpatterns = [
    path('', PersonListView.as_view(), name='index'),
    path('<int:pk>/', PersonDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', PersonUpdateView.as_view(), name='edit'),
    path('new/', PersonCreateView.as_view(), name='new'),
]
