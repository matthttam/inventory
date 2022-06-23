from django.contrib import admin
from .models import Building, Room


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ('name', 'number')


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('building', 'number',)
