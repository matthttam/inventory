from datetime import datetime
from django.forms import (
    CharField,
    Form,
    ModelForm,
    ModelChoiceField,
    DateField,
    TextInput,
    BooleanField,
)
from .models import DeviceAssignment
from people.models import Person
from devices.models import Device


class DeviceAssignmentForm(ModelForm):
    person = ModelChoiceField(queryset=Person.objects.all())
    device = ModelChoiceField(queryset=Device.objects.all())

    class Meta:

        model = DeviceAssignment
        fields = ["person", "device"]


class DeviceAssignmentTurninForm(ModelForm):
    class Meta:
        fields = ["id"]
        model = DeviceAssignment

    def save(self, commit=True, *args, **kwargs):
        self.instance.return_datetime = datetime.now()
        self.instance.save()
        return super().save(commit, *args, **kwargs)
