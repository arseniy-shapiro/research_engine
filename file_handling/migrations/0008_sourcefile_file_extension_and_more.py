# Generated by Django 4.2.3 on 2024-02-19 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_handling', '0007_alter_paperfile_uploading_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='sourcefile',
            name='file_extension',
            field=models.CharField(default='pdf', max_length=4),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='paperfile',
            name='file_extension',
            field=models.CharField(max_length=4),
        ),
    ]
