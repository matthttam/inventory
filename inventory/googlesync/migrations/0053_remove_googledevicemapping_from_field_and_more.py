# Generated by Django 4.0.5 on 2022-08-01 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('googlesync', '0052_alter_googledefaultschemaproperty_schema'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='googledevicemapping',
            name='from_field',
        ),
        migrations.RemoveField(
            model_name='googlepersonmapping',
            name='from_field',
        ),
        migrations.AddField(
            model_name='googledevicelinkmapping',
            name='from_field_original',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='googledevicemapping',
            name='from_field_original',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='googlepersonmapping',
            name='from_field_original',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
    ]
