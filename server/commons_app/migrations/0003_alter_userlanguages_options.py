# Generated by Django 4.2.2 on 2023-06-19 06:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('commons_app', '0002_userlanguages'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userlanguages',
            options={'verbose_name': 'language', 'verbose_name_plural': 'languages'},
        ),
    ]