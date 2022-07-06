# Generated by Django 4.0.5 on 2022-07-06 18:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0012_merge_20220706_1333'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='google_sync_profile',
        ),
        migrations.AlterField(
            model_name='device',
            name='google_id',
            field=models.CharField(blank=True, default=None, max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='devicemodel',
            name='manufacturer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='devices.devicemanufacturer'),
            preserve_default=False,
        ),
    ]
