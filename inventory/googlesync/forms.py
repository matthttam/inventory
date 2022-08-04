from django.forms import ModelForm, PasswordInput
from .models import GoogleConfig, GoogleServiceAccountConfig, GooglePersonMapping


class GoogleConfigForm(ModelForm):

    class Meta:

        model = GoogleConfig
        widgets = {
            'client_secret': PasswordInput()
        }
        fields = ['client_id', 'project_id', 'client_secret']


class GoogleServiceAccountConfigForm(ModelForm):

    class Meta:
        model = GoogleServiceAccountConfig
        fields = '__all__'


class GooglePersonMappingForm(ModelForm):

    class Meta:
        model = GooglePersonMapping
        fields = '__all__'
