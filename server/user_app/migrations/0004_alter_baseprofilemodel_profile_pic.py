# Generated by Django 4.2.2 on 2023-06-20 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0003_rename_userprofilemodel_baseprofilemodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseprofilemodel',
            name='profile_pic',
            field=models.ImageField(default='images/default.jpg', upload_to='media\\images'),
        ),
    ]
