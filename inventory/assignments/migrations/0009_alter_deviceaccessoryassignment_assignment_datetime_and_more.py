# Generated by Django 4.0.5 on 2022-08-06 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0008_alter_deviceaccessoryassignment_assignment_datetime_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deviceaccessoryassignment',
            name='assignment_datetime',
            field=models.DateTimeField(auto_now_add=True, verbose_name='assignment date'),
        ),
        migrations.AlterField(
            model_name='deviceassignment',
            name='assignment_datetime',
            field=models.DateTimeField(auto_now_add=True, verbose_name='assignment date'),
        ),
    ]
