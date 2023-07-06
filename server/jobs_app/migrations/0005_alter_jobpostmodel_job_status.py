# Generated by Django 4.2.2 on 2023-07-03 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs_app', '0004_alter_jobapplications_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobpostmodel',
            name='job_status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Open'), (1, 'Cancelled'), (2, 'Completed')], default=0, verbose_name='status of the job'),
        ),
    ]