# Generated by Django 4.2.2 on 2023-06-12 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('provider_app', '0012_alter_applyjobpostmodel_cover_letter_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='providermodel',
            name='profile_pic',
            field=models.ImageField(default='images/default.png', upload_to='media/provider_app_documents'),
        ),
    ]
