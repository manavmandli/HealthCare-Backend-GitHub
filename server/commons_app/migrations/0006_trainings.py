# Generated by Django 4.2.2 on 2023-06-21 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commons_app', '0005_rename_worktitles_jobtitles'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trainings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('training_name', models.CharField(max_length=255)),
            ],
        ),
    ]
