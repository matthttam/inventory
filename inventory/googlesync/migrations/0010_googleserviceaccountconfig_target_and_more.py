# Generated by Django 4.0.5 on 2022-06-24 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('googlesync', '0009_googleserviceaccountconfig_delegate'),
    ]

    operations = [
        migrations.AddField(
            model_name='googleserviceaccountconfig',
            name='target',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='googleserviceaccountconfig',
            name='delegate',
            field=models.EmailField(blank=True, default='', help_text='User account to impersonate when accessing Google. User must have rights to the resources needed.', max_length=255),
        ),
    ]