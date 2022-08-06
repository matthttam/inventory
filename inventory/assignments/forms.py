from django.forms import CharField, Form, ModelForm, ModelChoiceField, DateField, TextInput
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
        model = DeviceAssignment
        #fields = ('assignment_datetime',)
        fields = ['person','device','return_datetime']
    person = ModelChoiceField(queryset=Person.objects.all(), disabled=True)
    device = ModelChoiceField(queryset=Device.objects.all(), disabled=True)
    #return_datetime = DateField(widget=TextInput(attrs={'readonly':'readonly'}))
    #widgets={'assignment_datetime': CharField(disabled=True)}
    #return_date = DateField(disabled=True)

#class DeviceAssignmentTurninForm(Form):
#    return_datetime = DateField(disabled=True)
#    person = ModelChoiceField(queryset=Person.objects.all(), disabled=False)