# Generated by Django 4.0.5 on 2022-07-02 01:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0010_rename_device_model_deviceaccessory_device_models'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deviceaccessory',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
