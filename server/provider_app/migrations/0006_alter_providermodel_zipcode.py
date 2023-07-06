# Generated by Django 4.2.2 on 2023-06-12 05:07

from django.db import migrations, models
import provider_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('provider_app', '0005_alter_providermodel_i_9_form_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='providermodel',
            name='zipcode',
            field=models.IntegerField(default=1, validators=[provider_app.models.validate_zipcode]),
            preserve_default=False,
        ),
    ]
