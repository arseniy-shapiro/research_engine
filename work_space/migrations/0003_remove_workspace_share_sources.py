# Generated by Django 4.2.3 on 2024-01-22 14:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('work_space', '0002_remove_link_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workspace',
            name='share_sources',
        ),
    ]