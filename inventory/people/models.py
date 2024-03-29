from django.db import models
from django.db.models import F, Count, Q, When, Case, Value as V
from django.db.models.functions import Concat
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.urls import reverse

from auditlog.registry import auditlog
from auditlog.models import AuditlogHistoryField

from locations.models import Building, Room


class PersonStatus(models.Model):
    name = models.CharField(max_length=255)
    is_inactive = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Person statuses"

    def __str__(self):
        return f"{self.name}"


class PersonManager(models.Manager):
    def active(self):
        return self.filter(return_datetime=None)

    def get_queryset(self):
        qs = super().get_queryset()

        # Add their full name
        qs = qs.annotate(full_name=Concat(F("first_name"), V(" "), F("last_name")))
        # Add a count of outstanding assignments
        qs = qs.annotate(
            outstanding_assignment_count=Count(
                F("deviceassignments"),
                filter=Q(deviceassignments__return_datetime=None),
            )
        )

        qs = qs.annotate(
            is_currently_assigned=Case(
                When(outstanding_assignment_count__gt=0, then=True),
                default=False,
            )
        )

        # Set if the person is active
        qs = qs.annotate(
            is_active=Case(
                When(status__is_inactive=False, then=True),
                default=False,
            )
        )
        return qs


class Person(models.Model):
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, blank=True, default="")
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    internal_id = models.CharField(max_length=255, unique=True)
    type = models.ForeignKey("PersonType", on_delete=models.PROTECT)
    status = models.ForeignKey(PersonStatus, on_delete=models.PROTECT, default=1)
    buildings = models.ManyToManyField(Building, blank=True, related_name="people")
    rooms = models.ManyToManyField(Room, blank=True, related_name="people")
    google_id = models.CharField(max_length=255, blank=True)
    primary_building = models.ForeignKey(
        Building, blank=True, null=True, on_delete=models.SET_NULL
    )
    primary_room = models.ForeignKey(
        Room, blank=True, null=True, on_delete=models.SET_NULL
    )

    _buildings: list[Building] = None
    _rooms: list[Room] = None

    objects = PersonManager()
    history = AuditlogHistoryField()

    class Meta:
        verbose_name_plural = "People"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.internal_id})"

    def get_absolute_url(self):
        return reverse("people:detail", kwargs={"pk": self.pk})

    @property
    def display_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def building_list(self):
        return ", ".join([b.name for b in list(self.buildings.all().order_by("name"))])


@receiver(post_save, sender=Person)
def my_handler(sender, instance, **kwargs):
    if instance._buildings:
        instance.buildings.set(instance._buildings)
    if instance._rooms:
        instance.rooms.set(instance._rooms)


class PersonType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


# Audit Log Registrations
auditlog.register(Person)
