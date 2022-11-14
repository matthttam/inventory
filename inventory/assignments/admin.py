from django.contrib import admin
from .models import DeviceAssignment


@admin.register(DeviceAssignment)
class DeviceAssignmentAdmin(admin.ModelAdmin):
    list_display = (
        "device",
        "person",
        "assignment_datetime",
        "return_datetime",
    )
