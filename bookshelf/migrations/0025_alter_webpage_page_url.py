# Generated by Django 4.2.3 on 2023-11-23 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookshelf', '0024_rename_website_webpage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='webpage',
            name='page_url',
            field=models.CharField(max_length=100),
        ),
    ]