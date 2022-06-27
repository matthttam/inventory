from django.contrib import admin
from .models import GoogleConfig, GooglePersonSyncProfile, GooglePersonTranslation, GoogleServiceAccountConfig, GooglePersonMapping


@admin.register(GoogleConfig)
class GoogleConfigAdmin(admin.ModelAdmin):
    list_display = ("client_id",)


@admin.register(GoogleServiceAccountConfig)
class GoogleServiceAccountConfigAdmin(admin.ModelAdmin):
    list_display = ("client_email", "client_id")


@admin.register(GooglePersonMapping)
class GooglePersonMappingAdmin(admin.ModelAdmin):
    list_display = ('google_person_sync_profile', 'google_field', 'person_field', 'matching_priority')


@admin.register(GooglePersonTranslation)
class GooglePersonTranslationAdmin(admin.ModelAdmin):
    list_display = ('google_person_mapping',
                    'translate_from', 'translate_to')

@admin.register(GooglePersonSyncProfile)
class GooglePersonSyncProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'person_type', 'google_service_account_config')