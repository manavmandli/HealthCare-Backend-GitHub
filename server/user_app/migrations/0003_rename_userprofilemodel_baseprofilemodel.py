# Generated by Django 4.2.2 on 2023-06-20 05:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common_app', '0001_initial'),
        ('user_app', '0002_userprofilemodel_whatsapp_number'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserProfileModel',
            new_name='BaseProfileModel',
        ),
    ]
