# Generated by Django 4.2.2 on 2023-06-19 10:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0008_baseprofilemodel_about_baseprofilemodel_address_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='baseprofilemodel',
            options={'verbose_name': 'profile', 'verbose_name_plural': 'profiles'},
        ),
    ]