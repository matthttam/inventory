# Generated by Django 4.0.5 on 2022-08-01 17:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0005_room_unique_room_per_building'),
        ('people', '0010_alter_person_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='primary_building',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.building'),
        ),
        migrations.AddField(
            model_name='person',
            name='primary_room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.room'),
        ),
        migrations.AlterField(
            model_name='person',
            name='buildings',
            field=models.ManyToManyField(blank=True, related_name='people', to='locations.building'),
        ),
        migrations.AlterField(
            model_name='person',
            name='rooms',
            field=models.ManyToManyField(blank=True, related_name='people', to='locations.room'),
        ),
    ]
