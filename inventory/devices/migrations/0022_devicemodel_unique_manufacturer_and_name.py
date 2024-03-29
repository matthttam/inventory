# Generated by Django 4.0.5 on 2022-08-09 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0021_alter_devicemanufacturer_name'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='devicemodel',
            constraint=models.UniqueConstraint(fields=('manufacturer', 'name'), name='unique_manufacturer_and_name'),
        ),
    ]
