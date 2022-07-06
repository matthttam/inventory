from django.db import models


class Building(models.Model):
    name = models.CharField(max_length=255, unique=True)
    internal_id = models.CharField(max_length=255, blank=True, unique=True)
    acronym = models.CharField(max_length=255, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}"


class Room(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["number", "building"], name="unique_room_per_building"
            )
        ]

    number = models.CharField(max_length=255)
    building = models.ForeignKey(
        Building, on_delete=models.CASCADE, related_name="rooms"
    )
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.building.name} Room {self.number}"
