from django.contrib import admin
from .models import Device, DeviceManufacturer, DeviceModel, DeviceStatus


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("serial_number", "asset_id")


@admin.register(DeviceManufacturer)
class DeviceManufacturerAdmin(admin.ModelAdmin):
    pass


@admin.register(DeviceModel)
class DeviceModel(admin.ModelAdmin):
    pass


@admin.register(DeviceStatus)
class DeviceStatus(admin.ModelAdmin):
    pass
