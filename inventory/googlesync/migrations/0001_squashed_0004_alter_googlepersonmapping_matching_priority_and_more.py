# Generated by Django 4.0.5 on 2022-07-06 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [('googlesync', '0001_initial'), ('googlesync', '0002_googleserviceaccountconfig'), ('googlesync', '0003_googlepersonmapping'), ('googlesync', '0004_alter_googlepersonmapping_matching_priority_and_more')]

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GoogleConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_id', models.CharField(max_length=255)),
                ('project_id', models.CharField(max_length=255)),
                ('auth_uri', models.CharField(default='https://accounts.google.com/o/oauth2/auth', max_length=255)),
                ('token_uri', models.CharField(default='https://oauth2.googleapis.com/token', max_length=255)),
                ('auth_provider_x09_cert_url', models.CharField(default='https://www.googleapis.com/oauth2/v1/certs', max_length=255)),
                ('client_secret', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='GoogleServiceAccountConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(default='service_account', max_length=255)),
                ('project_id', models.CharField(max_length=255)),
                ('private_key_id', models.CharField(max_length=255)),
                ('private_key', models.TextField(max_length=2048)),
                ('client_email', models.CharField(max_length=255)),
                ('client_id', models.CharField(max_length=255)),
                ('auth_uri', models.CharField(default='https://accounts.google.com/o/oauth2/auth', max_length=255)),
                ('token_uri', models.CharField(default='https://oauth2.googleapis.com/token', max_length=255)),
                ('auth_provider_x09_cert_url', models.CharField(default='https://www.googleapis.com/oauth2/v1/certs', max_length=255)),
                ('client_x509_cert_url', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='GooglePersonMapping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('google_field', models.CharField(max_length=255)),
                ('person_field', models.CharField(choices=[('first_name', 'first name'), ('middle_name', 'middle name'), ('last_name', 'last name'), ('email', 'email'), ('internal_id', 'internal id'), ('type', 'type'), ('status', 'status')], max_length=255)),
                ('matching_priority', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)], unique=True)),
            ],
        ),
    ]
