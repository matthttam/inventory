# Generated by Django 4.0.5 on 2022-07-31 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('googlesync', '0046_googledefaultschema_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='googledefaultschema',
            name='description',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
    ]
