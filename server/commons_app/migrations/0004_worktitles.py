# Generated by Django 4.2.2 on 2023-06-19 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commons_app', '0003_alter_userlanguages_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkTitles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'work title',
                'verbose_name_plural': 'work titles',
            },
        ),
    ]
