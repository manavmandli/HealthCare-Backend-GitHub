# Generated by Django 4.2.2 on 2023-06-16 08:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facility_app', '0008_jobpostmodel_job_timings'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobpostmodel',
            name='city',
        ),
        migrations.RemoveField(
            model_name='jobpostmodel',
            name='zip_code',
        ),
    ]
