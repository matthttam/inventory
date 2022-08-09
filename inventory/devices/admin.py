from django.contrib import admin
from .models import (
    Device,
    DeviceAccessory,
    DeviceManufacturer,
    DeviceModel,
    DeviceStatus,
)


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("serial_number", "asset_id", "status")
    search_fields = ("serial_number", "asset_id")


@admin.register(DeviceManufacturer)
class DeviceManufacturerAdmin(admin.ModelAdmin):
    pass


@admin.register(DeviceModel)
class DeviceModelAdmin(admin.ModelAdmin):
    list_display = ("manufacturer", "name")
    search_fields = ("manufacturer__name", "name")


@admin.register(DeviceStatus)
class DeviceStatusAdmin(admin.ModelAdmin):
    pass


@admin.register(DeviceAccessory)
class DeviceAccessoryAdmin(admin.ModelAdmin):
    pass
