# Generated by Django 2.0.6 on 2018-11-20 18:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('imageboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transgression',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField()),
                ('banned_until', models.DateTimeField(help_text='Format: YYYY-MM-DD hh:mm. Eg. 2049-12-24 18:05')),
                ('reason', models.CharField(max_length=150)),
                ('global_ban', models.BooleanField(default=False)),
                ('banned_from', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='imageboard.Board')),
            ],
        ),
    ]
