from django.forms import ModelForm, ModelChoiceField
from .models import Person, PersonStatus, PersonType
from locations.models import Building, Room


class PersonForm(ModelForm):
    status = ModelChoiceField(queryset=PersonStatus.objects.all())
    type = ModelChoiceField(queryset=PersonType.objects.all())

    class Meta:
        model = Person
        fields = [
            "internal_id",
            "first_name",
            "middle_name",
            "last_name",
            "email",
            "type",
            "status",
        ]
