# Generated by Django 4.2.2 on 2023-07-08 11:15

from django.db import migrations, models
import tasks.models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0007_alter_groupmembers_invite_reason'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='filetask',
            field=models.FileField(blank=True, null=True, upload_to=tasks.models.user_directory_path),
        ),
    ]
