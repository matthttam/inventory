# Generated by Django 4.0.5 on 2022-07-11 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0002_person_buildings_person_rooms'),
    ]

    operations = [
        migrations.AddField(
            model_name='persontype',
            name='is_inactive',
            field=models.BooleanField(default=False),
        ),
    ]