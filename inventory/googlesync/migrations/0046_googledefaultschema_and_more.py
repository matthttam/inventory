# Generated by Django 4.0.5 on 2022-07-31 23:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('googlesync', '0045_alter_googlecustomschemafield_indexed_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoogleDefaultSchema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=1024)),
                ('schema_id', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=255)),
                ('service_account_config', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='default_schemas', to='googlesync.googleserviceaccountconfig')),
            ],
        ),
        migrations.AlterField(
            model_name='googlecustomschema',
            name='service_account_config',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='custom_schemas', to='googlesync.googleserviceaccountconfig'),
        ),
        migrations.CreateModel(
            name='GoogleDefaultSchemaProperty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('etag', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=1024)),
                ('ref', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ref', to='googlesync.googledefaultschema')),
                ('schema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schema', to='googlesync.googledefaultschema')),
            ],
        ),
    ]
