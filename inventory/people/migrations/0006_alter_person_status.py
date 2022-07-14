# Generated by Django 4.0.5 on 2022-06-24 20:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0005_person_google_id_alter_person_middle_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='status',
            field=models.ForeignKey(default='Active', on_delete=django.db.models.deletion.PROTECT, to='people.personstatus'),
        ),
    ]
