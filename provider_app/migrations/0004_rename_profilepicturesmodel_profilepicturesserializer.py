# Generated by Django 4.2.2 on 2023-06-28 09:18

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('provider_app', '0003_profilepicturesmodel'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProfilePicturesModel',
            new_name='ProfilePicturesSerializer',
        ),
    ]