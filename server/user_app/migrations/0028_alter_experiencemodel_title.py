# Generated by Django 4.2.2 on 2023-06-22 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0027_experiencemodel_work_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiencemodel',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]
