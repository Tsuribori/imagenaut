# Generated by Django 2.0.6 on 2018-08-16 13:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('imageboard', '0009_auto_20180814_1749'),
        ('moderation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transgression',
            name='banned_from',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='imageboard.Board'),
        ),
        migrations.AddField(
            model_name='transgression',
            name='global_ban',
            field=models.BooleanField(default=False),
        ),
    ]