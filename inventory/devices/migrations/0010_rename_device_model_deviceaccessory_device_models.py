# Generated by Django 4.0.5 on 2022-07-02 00:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0009_alter_devicestatus_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deviceaccessory',
            old_name='device_model',
            new_name='device_models',
        ),
    ]