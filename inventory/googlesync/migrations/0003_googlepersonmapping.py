# Generated by Django 4.0.5 on 2022-06-23 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('googlesync', '0002_googleserviceaccountconfig'),
    ]

    operations = [
        migrations.CreateModel(
            name='GooglePersonMapping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('google_field', models.CharField(max_length=255)),
                ('person_field', models.CharField(choices=[('id', 'ID'), ('first_name', 'first name'), ('middle_name', 'middle name'), ('last_name', 'last name'), ('email', 'email'), ('internal_id', 'internal id'), ('type', 'type'), ('status', 'status')], max_length=255)),
                ('matching_priority', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)])),
            ],
        ),
    ]
