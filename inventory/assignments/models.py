from django.db import models
from django.urls import reverse
from devices.models import Device, DeviceAccessory
from people.models import Person


class AssignmentAbstract(models.Model):
    assignment_datetime = models.DateTimeField(verbose_name="assignment date")
    return_datetime = models.DateTimeField(
        blank=True,
        null=True,
        default=None,
        verbose_name="return date",
    )
    person = models.ForeignKey(Person, on_delete=models.PROTECT)

    class Meta:
        abstract = True


class DeviceAssignment(AssignmentAbstract):
    device = models.ForeignKey(Device, on_delete=models.PROTECT)

    def get_absolute_url(self):
        return reverse("assignments:detail", kwargs={"pk": self.pk})


class DeviceAccessoryAssignment(AssignmentAbstract):
    device_accessory = models.ForeignKey(DeviceAccessory, on_delete=models.PROTECT)
