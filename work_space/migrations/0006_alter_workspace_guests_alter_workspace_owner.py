# Generated by Django 4.2.3 on 2023-12-13 10:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('work_space', '0005_rename_sharespacecode_sharesourcescode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workspace',
            name='guests',
            field=models.ManyToManyField(related_name='guest_work_spaces', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='workspace',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='work_spaces', to=settings.AUTH_USER_MODEL),
        ),
    ]
