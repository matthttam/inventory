from django.db import models
from django.urls import reverse
from django.db.models import F, Sum, Count, Q, When, Case, BooleanField

from auditlog.registry import auditlog
from auditlog.models import AuditlogHistoryField

from devices.models import Device, DeviceAccessory
from people.models import Person


class AssignmentManager(models.Manager):
    def outstanding(self):
        return self.filter(return_datetime=None)

    # def get_queryset(self):
    #    qs = super().get_queryset()
    #    qs = qs.annotate(
    #        is_outstanding=Case(
    #            When(return_datetime=None, then=True),
    #            default=False,
    #        )
    #    )
    #    return qs


class AssignmentAbstract(models.Model):
    assignment_datetime = models.DateTimeField(
        verbose_name="assignment date", auto_now=True
    )
    return_datetime = models.DateTimeField(
        blank=True,
        null=True,
        default=None,
        verbose_name="return date",
    )
    person = models.ForeignKey(
        Person,
        on_delete=models.PROTECT,
        related_query_name="%(class)s",
    )

    objects = AssignmentManager()

    class Meta:
        abstract = True

    @property
    def is_outstanding(self):
        return self.return_datetime is None


class DeviceAssignment(AssignmentAbstract):
    device = models.ForeignKey(Device, on_delete=models.PROTECT)
    history = AuditlogHistoryField()

    def get_absolute_url(self):
        return reverse("assignments:detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"Assignment {self.id}"


class DeviceAccessoryAssignment(AssignmentAbstract):
    device_accessory = models.ForeignKey(DeviceAccessory, on_delete=models.PROTECT)


# Audit Log Registrations
auditlog.register(DeviceAssignment)
