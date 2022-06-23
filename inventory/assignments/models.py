from django.db import models
from django.urls import reverse
from devices.models import Device, DeviceAccessory
from people.models import Person


class Assignment(models.Model):
    assignment_datetime = models.DateTimeField()
    return_datetime = models.DateTimeField(null=True)
    person = models.ForeignKey(Person, on_delete=models.PROTECT)

    class Meta:
        abstract = True


class DeviceAssignment(Assignment):
    device = models.ForeignKey(Device, on_delete=models.PROTECT)

    def get_absolute_url(self):
        return reverse('assignments:detail', kwargs={'pk': self.pk})


class DeviceAccessoryAssignment(Assignment):
    device_accessory = models.ForeignKey(
        DeviceAccessory, on_delete=models.PROTECT)
