# Generated by Django 4.2.2 on 2023-06-16 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facility_app', '0007_rename_job_title_jobpostmodel_title_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobpostmodel',
            name='job_timings',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Part time'), (1, 'Full time')], default=1),
            preserve_default=False,
        ),
    ]
