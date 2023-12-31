# Generated by Django 4.2.2 on 2023-07-07 01:33

from django.db import migrations, models
import tasks.models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_xtorage'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='filetask',
            field=models.FileField(null=True, upload_to=tasks.models.user_directory_path),
        ),
        migrations.AlterField(
            model_name='xtorage',
            name='upload',
            field=models.FileField(upload_to='example/'),
        ),
    ]
