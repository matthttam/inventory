from django.db import models


class Building(models.Model):
    name = models.CharField(max_length=255)
    number = models.CharField(max_length=255, blank=True)
    acronym = models.CharField(max_length=255, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}"


class Room(models.Model):
    number = models.CharField(max_length=255)
    building = models.ForeignKey(
        Building, on_delete=models.CASCADE, related_name='rooms')
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.building.name} Room {self.number}"
