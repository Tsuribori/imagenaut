# Generated by Django 2.0.6 on 2018-09-23 10:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imageboard', '0005_auto_20180923_1004'),
    ]

    operations = [
        migrations.RenameField(
            model_name='thread',
            old_name='video',
            new_name='embed',
        ),
        migrations.RenameField(
            model_name='userpost',
            old_name='video',
            new_name='embed',
        ),
    ]
