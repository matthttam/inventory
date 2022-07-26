# Generated by Django 4.0.5 on 2022-07-26 16:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0010_alter_person_options'),
        ('assignments', '0006_alter_deviceaccessoryassignment_person_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deviceaccessoryassignment',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_query_name='%(class)s', to='people.person'),
        ),
        migrations.AlterField(
            model_name='deviceassignment',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_query_name='%(class)s', to='people.person'),
        ),
    ]
