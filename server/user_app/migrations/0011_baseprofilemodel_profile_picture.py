# Generated by Django 4.2.2 on 2023-06-20 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0010_baseprofilemodel_languages'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseprofilemodel',
            name='profile_picture',
            field=models.ImageField(default='static/img/default_user.png', upload_to='profile_pictures'),
        ),
    ]
