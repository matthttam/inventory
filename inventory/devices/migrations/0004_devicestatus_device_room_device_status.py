# Generated by Django 4.0.5 on 2022-06-22 14:27

from django.db import migrations, models
import django.db.models.deletion


def populate_device_status_field(apps, schema_editor):
    DeviceStatus = apps.get_model('devices', 'DeviceStatus')
    device_status = DeviceStatus(name='Active')
    device_status.save()


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0001_initial'),
        ('devices', '0003_alter_device_google_enrollment_time_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.RunPython(populate_device_status_field),
        migrations.AddField(
            model_name='device',
            name='room',
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.room'),
        ),
        migrations.AddField(
            model_name='device',
            name='status',
            field=models.ForeignKey(
                default='1', on_delete=django.db.models.deletion.PROTECT, to='devices.devicestatus'),
            preserve_default=False,
        ),
    ]
