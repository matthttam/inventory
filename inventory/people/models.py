from django.db import models
from django.urls import reverse
from locations.models import Room, Building


class Person(models.Model):
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    internal_id = models.CharField(max_length=255, unique=True)
    type = models.ForeignKey("PersonType", on_delete=models.PROTECT)
    status = models.ForeignKey("PersonStatus", on_delete=models.PROTECT)
    buildings = models.ManyToManyField(Building)
    rooms = models.ManyToManyField(Room)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.internal_id})"

    def get_absolute_url(self):
        return reverse("people:detail", kwargs={"pk": self.pk})

    def display_name(self):
        return f"{self.first_name} {self.last_name}"


class PersonType(models.Model):
    name = models.CharField(max_length=255)
    is_inactive = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"


class PersonStatus(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Person statuses"

    def __str__(self):
        return f"{self.name}"
