# Generated by Django 4.2.2 on 2023-06-12 11:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('provider_app', '0018_alter_applyjobpostmodel_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='providerratingmodel',
            name='provider_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='provider_app.providermodel'),
        ),
    ]