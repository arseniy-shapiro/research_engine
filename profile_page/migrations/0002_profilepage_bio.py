# Generated by Django 4.2.3 on 2023-12-06 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile_page', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profilepage',
            name='bio',
            field=models.CharField(default='My bio', max_length=200),
            preserve_default=False,
        ),
    ]
