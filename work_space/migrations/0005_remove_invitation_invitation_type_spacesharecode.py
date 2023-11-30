# Generated by Django 4.2.3 on 2023-11-30 13:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('work_space', '0004_invitation_invitation_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invitation',
            name='invitation_type',
        ),
        migrations.CreateModel(
            name='SpaceShareCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=15, unique=True)),
                ('work_space', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='work_space.workspace')),
            ],
        ),
    ]
