# Generated by Django 4.2.2 on 2023-06-19 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commons_app', '0005_rename_worktitles_jobtitles'),
        ('user_app', '0009_alter_baseprofilemodel_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseprofilemodel',
            name='languages',
            field=models.ManyToManyField(to='commons_app.userlanguages'),
        ),
    ]