# Generated by Django 4.2.2 on 2023-06-16 06:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('commons_app', '0001_initial'),
        ('provider_app', '0022_alter_provideraverageratingmodel_average_rating_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='providermodel',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commons_app.citymodel'),
        ),
    ]
