# Generated by Django 2.0.6 on 2018-08-18 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imageboard', '0009_auto_20180814_1749'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='reported',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userpost',
            name='reported',
            field=models.BooleanField(default=False),
        ),
    ]
