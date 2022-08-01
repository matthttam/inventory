from django.contrib import admin
from .models import Person, PersonType, PersonStatus


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    search_fields = (
        "internal_id",
        "first_name",
        "middle_name",
        "last_name",
        "email",
    )
    list_display = (
        "internal_id",
        "first_name",
        "middle_name",
        "last_name",
        "email",
        "type",
        "status",
        "primary_building",
    )


@admin.register(PersonType)
class PersonTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(PersonStatus)
class PersonStatusAdmin(admin.ModelAdmin):
    pass
