# Generated by Django 4.2.3 on 2023-11-17 16:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookshelf', '0013_rename_journal_number_article_issue_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='endnote',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookshelf.source'),
        ),
    ]