# Generated by Django 4.0.5 on 2022-08-01 15:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('googlesync', '0057_googleserviceaccountconfig_device_initialized'),
    ]

    operations = [
        migrations.RenameField(
            model_name='googledevicemapping',
            old_name='from_field',
            new_name='from_field_old',
        ),
        migrations.RemoveField(
            model_name='googledevicelinkmapping',
            name='from_field_original',
        ),
        migrations.RemoveField(
            model_name='googledevicemapping',
            name='from_field_original',
        ),
        migrations.RemoveField(
            model_name='googlepersonmapping',
            name='from_field_original',
        ),
    ]