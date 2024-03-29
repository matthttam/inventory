# Generated by Django 4.0.5 on 2022-08-01 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('googlesync', '0060_remove_googledevicemapping_from_field_old_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='googlepersonmapping',
            name='to_field',
            field=models.CharField(choices=[('first_name', 'first name'), ('middle_name', 'middle name'), ('last_name', 'last name'), ('email', 'email'), ('internal_id', 'internal id'), ('type', 'type'), ('status', 'status'), ('google_id', 'google id'), ('primary_building', 'primary building'), ('primary_room', 'primary room')], max_length=255),
        ),
    ]
