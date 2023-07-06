# Generated by Django 4.2.2 on 2023-06-29 10:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs_app', '0002_alter_jobapplications_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobapplications',
            name='status',
            field=models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(3)]),
        ),
    ]