# Generated by Django 4.0.5 on 2022-08-06 01:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('googlesync', '0067_remove_googledevicelinkmapping_unique_sync_profile_and_to_field_in_googledevicelinkmapping_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='googledevicelinkmapping',
            name='unique_sync_profile_and_to_field_in_googledevicelinkmapping',
        ),
        migrations.RemoveConstraint(
            model_name='googledevicemapping',
            name='unique_sync_profile_and_to_field_in_googledevicemapping',
        ),
        migrations.RemoveConstraint(
            model_name='googlepersonmapping',
            name='unique_sync_profile_and_to_field_in_googlepersonmapping',
        ),
    ]
