# Generated by Django 4.0.5 on 2022-06-22 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0002_building_acronym_building_active_room_active'),
        ('people', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='buildings',
            field=models.ManyToManyField(to='locations.building'),
        ),
        migrations.AddField(
            model_name='person',
            name='rooms',
            field=models.ManyToManyField(to='locations.room'),
        ),
    ]