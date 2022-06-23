from django.urls import path, include
from .views import *
from .views import GoogleConfigCreateUpdateView, GoogleServiceAccountConfigCreateUpdateView, GooglePersonMapping

app_name = 'googlesync'
urlpatterns = [
    path('', GoogleConfigCreateUpdateView.as_view(), name='config'),
    path('serviceaccount/', GoogleServiceAccountConfigCreateUpdateView.as_view(),
         name='service_account_config'),
    path('personmapping/', GooglePersonMappingCreateUpdateView.as_view(),
         name='person_mapping'),
]
