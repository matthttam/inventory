from django.contrib import admin
from .models import GoogleConfig, GoogleServiceAccountConfig
from .models import (
    GooglePersonSyncProfile,
    GooglePersonTranslation,
    GooglePersonMapping,
)
from .models import (
    GoogleDeviceSyncProfile,
    GoogleDeviceTranslation,
    GoogleDeviceMapping,
)


@admin.register(GoogleConfig)
class GoogleConfigAdmin(admin.ModelAdmin):
    list_display = ("client_id",)


@admin.register(GoogleServiceAccountConfig)
class GoogleServiceAccountConfigAdmin(admin.ModelAdmin):
    list_display = ("client_email", "client_id")


@admin.register(GooglePersonMapping)
class GooglePersonMappingAdmin(admin.ModelAdmin):
    list_display = (
        "google_person_sync_profile",
        "google_field",
        "person_field",
        "matching_priority",
    )


@admin.register(GooglePersonTranslation)
class GooglePersonTranslationAdmin(admin.ModelAdmin):
    list_display = ("google_person_mapping", "translate_from", "translate_to")


@admin.register(GooglePersonSyncProfile)
class GooglePersonSyncProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "person_type", "google_service_account_config")


@admin.register(GoogleDeviceMapping)
class GoogleDeviceMappingAdmin(admin.ModelAdmin):
    list_display = (
        "google_device_sync_profile",
        "google_field",
        "device_field",
        "matching_priority",
    )


@admin.register(GoogleDeviceTranslation)
class GoogleDeviceTranslationAdmin(admin.ModelAdmin):
    list_display = ("google_device_mapping", "translate_from", "translate_to")


@admin.register(GoogleDeviceSyncProfile)
class GoogleDeviceSyncProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "google_service_account_config")
