# Generated by Django 4.0.5 on 2022-08-09 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0020_alter_device_asset_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devicemanufacturer',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
