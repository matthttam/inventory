# Generated by Django 4.0.5 on 2022-08-06 01:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0009_alter_deviceaccessoryassignment_assignment_datetime_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='deviceassignment',
            options={'permissions': (('turnin_deviceassignment', 'Can turn in a device assignment'),)},
        ),
    ]
