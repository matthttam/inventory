# Generated by Django 4.0.5 on 2022-06-21 20:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceManufacturer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='DeviceModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('manufacturer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='devices.devicemanufacturer')),
            ],
        ),
        migrations.CreateModel(
            name='DeviceAccessory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('device_model', models.ManyToManyField(to='devices.devicemodel')),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_number', models.CharField(max_length=255, unique=True)),
                ('asset_id', models.CharField(max_length=255, unique=True)),
                ('notes', models.CharField(blank=True, max_length=255)),
                ('google_status', models.CharField(max_length=255)),
                ('google_organization_unit', models.CharField(max_length=255)),
                ('google_enrollment_time', models.DateTimeField()),
                ('google_last_policy_sync', models.DateTimeField()),
                ('google_location', models.CharField(blank=True, max_length=255)),
                ('google_most_recent_user', models.CharField(max_length=255)),
                ('device_model', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='devices.devicemodel')),
            ],
        ),
    ]
