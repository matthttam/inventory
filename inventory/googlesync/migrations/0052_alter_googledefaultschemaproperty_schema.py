# Generated by Django 4.0.5 on 2022-08-01 02:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('googlesync', '0051_remove_googledefaultschemaproperty_ref_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='googledefaultschemaproperty',
            name='schema',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='properties', to='googlesync.googledefaultschema'),
        ),
    ]
