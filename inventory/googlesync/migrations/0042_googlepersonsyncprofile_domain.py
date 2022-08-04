# Generated by Django 4.0.5 on 2022-07-29 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('googlesync', '0041_alter_googledevicelinkmapping_matching_priority_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='googlepersonsyncprofile',
            name='domain',
            field=models.CharField(blank=True, default='', help_text='Filter by domain of users. If left blank users of any domain for your Google Customer will be included.', max_length=1024),
        ),
    ]