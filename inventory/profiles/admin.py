from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class DeviceAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "timezone",
    )
