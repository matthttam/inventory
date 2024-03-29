from django.contrib import admin
from .models import Building, Room


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ("name", "acronym", "internal_id")


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        "building",
        "number",
    )
