# Generated by Django 4.2.2 on 2023-06-23 05:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('commons_app', '0007_alter_trainings_options'),
        ('facility_app', '0011_remove_jobpostmodel_open_for'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobpostmodel',
            name='city',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='commons_app.citymodel'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='jobpostmodel',
            name='zip_code',
            field=models.CharField(default=1, max_length=9),
            preserve_default=False,
        ),
    ]
