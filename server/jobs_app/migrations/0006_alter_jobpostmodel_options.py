# Generated by Django 4.2.2 on 2023-07-04 11:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs_app', '0005_alter_jobpostmodel_job_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='jobpostmodel',
            options={'ordering': ['-posted_on'], 'verbose_name': 'Manage Job Post', 'verbose_name_plural': 'Manage Job Posting'},
        ),
    ]
