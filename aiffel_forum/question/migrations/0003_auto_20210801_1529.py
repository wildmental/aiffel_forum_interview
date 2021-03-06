# Generated by Django 3.2.5 on 2021-08-01 06:29

import datetime
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('question', '0002_auto_20210801_0114'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='likes',
        ),
        migrations.AddField(
            model_name='question',
            name='like_users',
            field=models.ManyToManyField(blank=True, related_name='like_questions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comment',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 1, 15, 29, 10, 961402)),
        ),
        migrations.AlterField(
            model_name='question',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 1, 15, 29, 10, 959408)),
        ),
    ]
