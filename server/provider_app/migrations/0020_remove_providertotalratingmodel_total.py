# Generated by Django 4.2.2 on 2023-06-12 12:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('provider_app', '0019_alter_providerratingmodel_provider_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='providertotalratingmodel',
            name='total',
        ),
    ]