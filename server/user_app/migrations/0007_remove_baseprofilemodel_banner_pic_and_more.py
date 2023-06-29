# Generated by Django 4.2.2 on 2023-06-20 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0006_profilepicmodel_alter_baseprofilemodel_profile_pic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='baseprofilemodel',
            name='banner_pic',
        ),
        migrations.RemoveField(
            model_name='baseprofilemodel',
            name='profile_pic',
        ),
        migrations.AddField(
            model_name='profilepicmodel',
            name='banner_pic',
            field=models.ImageField(null=True, upload_to='media\\images'),
        ),
    ]
