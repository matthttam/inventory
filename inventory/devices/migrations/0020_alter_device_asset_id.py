# Generated by Django 4.0.5 on 2022-08-09 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0019_alter_deviceaccessory_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='asset_id',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]