# Generated by Django 4.2.3 on 2024-01-20 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paper_work', '0003_alter_paper_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paper',
            name='citation_style',
            field=models.CharField(default='APA', max_length=10),
        ),
    ]