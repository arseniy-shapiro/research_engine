# Generated by Django 4.2.3 on 2023-12-13 10:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('work_space', '0004_remove_workspace_citation_style'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ShareSpaceCode',
            new_name='ShareSourcesCode',
        ),
    ]
