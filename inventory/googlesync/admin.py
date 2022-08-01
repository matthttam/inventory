from django.contrib import admin
from .models import (
    GoogleConfig,
    GoogleDeviceLinkMapping,
    GoogleCustomSchema,
    GoogleCustomSchemaField,
    GoogleServiceAccountConfig,
    GooglePersonSyncProfile,
    GooglePersonTranslation,
    GooglePersonMapping,
    GoogleDeviceSyncProfile,
    GoogleDeviceTranslation,
    GoogleDeviceMapping,
    GoogleDevice,
    GoogleDefaultSchema,
    GoogleDefaultSchemaProperty,
)


@admin.register(GoogleDevice)
class GoogleDevice(admin.ModelAdmin):
    list_display = [field.name for field in GoogleDevice._meta.get_fields()]


@admin.register(GoogleConfig)
class GoogleConfigAdmin(admin.ModelAdmin):
    list_display = ("client_id",)


@admin.register(GoogleServiceAccountConfig)
class GoogleServiceAccountConfigAdmin(admin.ModelAdmin):
    list_display = ("client_email", "client_id")


@admin.register(GooglePersonMapping)
class GooglePersonMappingAdmin(admin.ModelAdmin):
    list_display = (
        "sync_profile",
        "from_field",
        "to_field",
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
        "sync_profile",
        "from_field_original",
        "to_field",
    )


@admin.register(GoogleDeviceLinkMapping)
class GoogleDeviceLinkMappingAdmin(admin.ModelAdmin):
    list_display = (
        "sync_profile",
        "from_field",
        "to_field",
        "matching_priority",
    )


@admin.register(GoogleDeviceTranslation)
class GoogleDeviceTranslationAdmin(admin.ModelAdmin):
    list_display = ("google_device_mapping", "translate_from", "translate_to")


@admin.register(GoogleDeviceSyncProfile)
class GoogleDeviceSyncProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "google_service_account_config")


@admin.register(GoogleCustomSchema)
class GoogleCustomSchema(admin.ModelAdmin):
    # pass
    list_display = ("display_name",)

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(GoogleCustomSchemaField)
class GoogleCustomSchemaField(admin.ModelAdmin):

    list_display = ("__str__", "field_type", "indexed", "multi_valued")

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(GoogleDefaultSchema)
class GoogleDefaultSchema(admin.ModelAdmin):
    list_display = (
        "schema_id",
        "description",
    )

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(GoogleDefaultSchemaProperty)
class GoogleDefaultSchemaProperty(admin.ModelAdmin):

    list_display = ("__str__", "etag", "type", "description")

    def has_change_permission(self, request, obj=None):
        return False
