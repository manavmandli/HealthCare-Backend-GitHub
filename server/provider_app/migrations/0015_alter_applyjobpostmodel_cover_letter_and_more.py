# Generated by Django 4.2.2 on 2023-06-12 08:32

from django.db import migrations, models
import provider_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('provider_app', '0014_alter_providermodel_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applyjobpostmodel',
            name='cover_letter',
            field=models.FileField(upload_to='', validators=[provider_app.models.validate_file_size]),
        ),
        migrations.AlterField(
            model_name='providermodel',
            name='I_9_Form',
            field=models.FileField(upload_to='', validators=[provider_app.models.validate_file_size]),
        ),
        migrations.AlterField(
            model_name='providermodel',
            name='cds_license',
            field=models.FileField(upload_to='', validators=[provider_app.models.validate_file_size]),
        ),
        migrations.AlterField(
            model_name='providermodel',
            name='check_registry',
            field=models.FileField(upload_to='', validators=[provider_app.models.validate_file_size]),
        ),
        migrations.AlterField(
            model_name='providermodel',
            name='cpr_certification',
            field=models.FileField(help_text='BHT/ Medical staff', upload_to='', validators=[provider_app.models.validate_file_size]),
        ),
        migrations.AlterField(
            model_name='providermodel',
            name='dea_license',
            field=models.FileField(upload_to='', validators=[provider_app.models.validate_file_size]),
        ),
        migrations.AlterField(
            model_name='providermodel',
            name='drug_screen',
            field=models.FileField(upload_to='', validators=[provider_app.models.validate_file_size]),
        ),
        migrations.AlterField(
            model_name='providermodel',
            name='flu_vaccination',
            field=models.FileField(upload_to='', validators=[provider_app.models.validate_file_size]),
        ),
        migrations.AlterField(
            model_name='providermodel',
            name='id_proof',
            field=models.FileField(upload_to='', validators=[provider_app.models.validate_file_size]),
        ),
        migrations.AlterField(
            model_name='providermodel',
            name='immunization_record',
            field=models.FileField(upload_to='', validators=[provider_app.models.validate_file_size]),
        ),
        migrations.AlterField(
            model_name='providermodel',
            name='license_and_verfication',
            field=models.FileField(upload_to='', validators=[provider_app.models.validate_file_size]),
        ),
        migrations.AlterField(
            model_name='providermodel',
            name='npdb',
            field=models.FileField(help_text='MD Only', upload_to='', validators=[provider_app.models.validate_file_size]),
        ),
        migrations.AlterField(
            model_name='providermodel',
            name='orignal_degree',
            field=models.FileField(upload_to='', validators=[provider_app.models.validate_file_size]),
        ),
        migrations.AlterField(
            model_name='providermodel',
            name='resume',
            field=models.FileField(upload_to='', validators=[provider_app.models.validate_file_size]),
        ),
        migrations.AlterField(
            model_name='providermodel',
            name='tb_screening',
            field=models.FileField(upload_to='', validators=[provider_app.models.validate_file_size]),
        ),
        migrations.AlterField(
            model_name='providermodel',
            name='w4_w9_1099',
            field=models.FileField(help_text='w4/ w9/ 1099', upload_to='', validators=[provider_app.models.validate_file_size]),
        ),
    ]
