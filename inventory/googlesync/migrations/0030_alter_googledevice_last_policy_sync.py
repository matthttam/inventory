# Generated by Django 4.0.5 on 2022-07-13 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('googlesync', '0029_alter_googledevicemapping_to_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='googledevice',
            name='last_policy_sync',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]
