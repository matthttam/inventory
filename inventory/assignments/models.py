from django.db import models
from django.urls import reverse

from auditlog.registry import auditlog
from auditlog.models import AuditlogHistoryField

from devices.models import Device, DeviceAccessory
from people.models import Person
from django.db.models import CharField, Value as V, Q, F, Case, When, Prefetch


class AssignmentManager(models.Manager):
    def outstanding(self):
        """Assignments that have not been returned"""
        return self.filter(return_datetime=None)

    def get_queryset(self):
        qs = super().get_queryset()

        # Add is_outstanding
        qs = qs.annotate(
            is_outstanding=Case(
                When(return_datetime=None, then=True),
                default=False,
            )
        )

        return qs


class AssignmentAbstract(models.Model):
    assignment_datetime = models.DateTimeField(
        verbose_name="assignment date", auto_now_add=True
    )
    return_datetime = models.DateTimeField(
        blank=True,
        null=True,
        default=None,
        verbose_name="return date",
    )

    objects = AssignmentManager()

    class Meta:
        abstract = True

    # @property
    # def is_outstanding(self):
    #    return self.return_datetime is None


class DeviceAssignment(AssignmentAbstract):
    device = models.ForeignKey(
        Device, on_delete=models.PROTECT, related_name="deviceassignments"
    )
    person = models.ForeignKey(
        Person,
        on_delete=models.PROTECT,
        related_name="deviceassignments",
    )
    history = AuditlogHistoryField()

    class Meta:
        permissions = (("turnin_deviceassignment", "Can turn in a device assignment"),)

    def get_absolute_url(self):
        return reverse("assignments:detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"Assignment {self.id}"


class DeviceAccessoryAssignment(AssignmentAbstract):
    device_accessory = models.ForeignKey(DeviceAccessory, on_delete=models.PROTECT)
    person = models.ForeignKey(
        Person,
        on_delete=models.PROTECT,
        related_name="deviceaccessoryassignments",
    )


# Audit Log Registrations
auditlog.register(DeviceAssignment)
