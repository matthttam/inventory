from django.contrib import admin
from .models import GoogleConfig, GooglePersonTranslation, GoogleServiceAccountConfig, GooglePersonMapping


@admin.register(GoogleConfig)
class GoogleConfigAdmin(admin.ModelAdmin):
    list_display = ("client_id",)


@admin.register(GoogleServiceAccountConfig)
class GoogleServiceAccountConfigAdmin(admin.ModelAdmin):
    list_display = ("client_email", "client_id")


@admin.register(GooglePersonMapping)
class GooglePersonMappingAdmin(admin.ModelAdmin):
    list_display = ('google_field', 'person_field', 'matching_priority')


@admin.register(GooglePersonTranslation)
class GooglePersonTranslationAdmin(admin.ModelAdmin):
    list_display = ('person_type', 'person_field',
                    'translate_from', 'translate_to')
