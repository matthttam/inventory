# Generated by Django 4.0.5 on 2022-06-30 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0003_remove_building_number_building_internal_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='building',
            name='acronym',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
