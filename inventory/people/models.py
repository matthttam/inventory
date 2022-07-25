from django.db import models
from django.urls import reverse
from locations.models import Room, Building
from django.db.models.signals import post_save
from django.dispatch import receiver


class PersonStatus(models.Model):
    name = models.CharField(max_length=255)
    is_inactive = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Person statuses"

    def __str__(self):
        return f"{self.name}"


class Person(models.Model):
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, blank=True, default="")
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    internal_id = models.CharField(max_length=255, unique=True)
    type = models.ForeignKey("PersonType", on_delete=models.PROTECT)
    status = models.ForeignKey(PersonStatus, on_delete=models.PROTECT, default=1)
    buildings = models.ManyToManyField(Building, blank=True)
    rooms = models.ManyToManyField(Room, blank=True)
    google_id = models.CharField(max_length=255, blank=True)
    _buildings: list[Building] = None
    _rooms: list[Room] = None

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
        return ", ".join([b.name for b in list(self.buildings.all())])


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
