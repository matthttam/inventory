from django.forms import ModelForm, ModelChoiceField
from .models import Device
from .models import DeviceModel
from locations.models import Building, Room


class DeviceForm(ModelForm):
    device_model = ModelChoiceField(queryset=DeviceModel.objects.all())
    building = ModelChoiceField(queryset=Building.objects.filter(active=True))
    room = ModelChoiceField(queryset=Room.objects.filter(active=True))

    class Meta:
        model = Device
        fields = ['serial_number', 'asset_id',
                  'device_model', 'building', 'room', 'notes']
