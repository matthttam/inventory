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
    DeviceBuildingToGoogleOUMapping,
)


@admin.register(GoogleDevice)
class GoogleDeviceAdmin(admin.ModelAdmin):
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

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        print(db_field.name)
        if db_field.name == "from_field":
            kwargs["queryset"] = GoogleDefaultSchemaProperty.objects.filter(
                schema__schema_id__in=["User", "UserName"]
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


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
        "from_field",
        "to_field",
        "matching_priority",
    )

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == "from_field":
            kwargs["queryset"] = GoogleDefaultSchemaProperty.objects.filter(
                schema__schema_id__in=["ChromeOsDevice"]
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


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
class GoogleCustomSchemaAdmin(admin.ModelAdmin):
    # pass
    list_display = ("display_name",)

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(GoogleCustomSchemaField)
class GoogleCustomSchemaFieldAdmin(admin.ModelAdmin):

    list_display = ("__str__", "field_type", "indexed", "multi_valued")

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(GoogleDefaultSchema)
class GoogleDefaultSchemaAdmin(admin.ModelAdmin):
    list_display = (
        "schema_id",
        "description",
    )

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(GoogleDefaultSchemaProperty)
class GoogleDefaultSchemaPropertyAdmin(admin.ModelAdmin):

    list_display = ("schema", "__str__", "etag", "type", "description")

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(DeviceBuildingToGoogleOUMapping)
class DeviceBuildingToGoogleOUMappingAdmin(admin.ModelAdmin):

    list_display = ("person_type", "building", "organization_unit")
