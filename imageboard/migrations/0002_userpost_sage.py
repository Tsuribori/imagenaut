# Generated by Django 2.0.6 on 2018-08-11 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imageboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpost',
            name='sage',
            field=models.BooleanField(default=False),
        ),
    ]
