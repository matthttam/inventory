# Generated by Django 4.0.5 on 2022-08-01 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('googlesync', '0055_googledefaultschemaproperty_format'),
    ]

    operations = [
        migrations.AddField(
            model_name='googledevicemapping',
            name='from_field',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
    ]