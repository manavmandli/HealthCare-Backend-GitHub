# Generated by Django 4.2.2 on 2023-06-19 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commons_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserLanguages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(max_length=255)),
            ],
        ),
    ]
