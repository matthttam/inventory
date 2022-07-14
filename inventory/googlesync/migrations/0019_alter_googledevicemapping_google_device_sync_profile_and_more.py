# Generated by Django 4.0.5 on 2022-06-28 12:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('googlesync', '0018_googledevicemapping_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='googledevicemapping',
            name='google_device_sync_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='googlesync.googledevicesyncprofile'),
        ),
        migrations.AddConstraint(
            model_name='googledevicemapping',
            constraint=models.UniqueConstraint(fields=('google_device_sync_profile', 'device_field'), name='unique_google_device_sync_profile_and_device_field'),
        ),
    ]