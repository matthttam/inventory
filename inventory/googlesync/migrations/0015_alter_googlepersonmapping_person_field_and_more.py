# Generated by Django 4.0.5 on 2022-06-27 15:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('googlesync', '0014_googlepersonsyncprofile_google_query'),
    ]

    operations = [
        migrations.AlterField(
            model_name='googlepersonmapping',
            name='person_field',
            field=models.CharField(choices=[('first_name', 'first name'), ('middle_name', 'middle name'), ('last_name', 'last name'), ('email', 'email'), ('internal_id', 'internal id'), ('type', 'type'), ('status', 'status'), ('google_id', 'google id')], max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='googlepersontranslation',
            name='person_field',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='googlesync.googlepersonmapping', to_field='person_field'),
        ),
    ]