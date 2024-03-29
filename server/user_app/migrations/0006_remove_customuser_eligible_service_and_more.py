# Generated by Django 4.2.2 on 2023-06-16 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0005_alter_customuser_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='eligible_service',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('admin', 'admin'), ('facility', 'facility'), ('provider', 'provider')], default='provider', max_length=8),
            preserve_default=False,
        ),
    ]
