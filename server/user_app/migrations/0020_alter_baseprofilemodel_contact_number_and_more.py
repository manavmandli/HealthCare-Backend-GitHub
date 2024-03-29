# Generated by Django 4.2.2 on 2023-06-22 05:38

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0019_remove_baseprofilemodel_facebook_link_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseprofilemodel',
            name='contact_number',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=11, region=None),
        ),
        migrations.AlterField(
            model_name='baseprofilemodel',
            name='whatsapp_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=11, null=True, region=None),
        ),
    ]
