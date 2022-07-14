# Generated by Django 4.0.5 on 2022-06-28 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('googlesync', '0019_alter_googledevicemapping_google_device_sync_profile_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='googledevicemapping',
            name='device_field',
            field=models.CharField(choices=[('serial_number', 'serial number'), ('asset_id', 'asset id'), ('notes', 'notes'), ('status', 'status'), ('google_sync_profile', 'google sync profile'), ('google_id', 'google id'), ('google_status', 'google status'), ('google_organization_unit', 'google organization unit'), ('google_enrollment_time', 'google enrollment time'), ('google_last_policy_sync', 'google last policy sync'), ('google_location', 'google location'), ('google_most_recent_user', 'google most recent user'), ('device_model', 'device model'), ('building', 'building'), ('room', 'room')], max_length=255),
        ),
    ]
