from django.forms import ModelForm, ModelChoiceField
from .models import DeviceAssignment
from people.models import Person
from devices.models import Device


class DeviceAssignmentForm(ModelForm):
    person = ModelChoiceField(queryset=Person.objects.all())
    device = ModelChoiceField(queryset=Device.objects.all())

    class Meta:

        model = DeviceAssignment
        fields = ['person', 'device']
