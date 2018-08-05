# Generated by Django 2.0.6 on 2018-07-30 14:41

from django.db import migrations, models
import django.db.models.deletion
import imageboard.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=31, unique=True)),
                ('slug', models.SlugField(max_length=31, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thread_number', models.PositiveIntegerField(default=imageboard.models.Thread.get_thread_number, unique=True)),
                ('subject', models.CharField(blank=True, max_length=50)),
                ('name', models.CharField(default='Anonymous', max_length=20)),
                ('time_made', models.DateTimeField(auto_now_add=True)),
                ('post', models.CharField(max_length=5000)),
                ('bumb_order', models.DateTimeField(auto_now=True)),
                ('ip_address', models.GenericIPAddressField()),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='imageboard.Board')),
            ],
            options={
                'ordering': ['-bumb_order'],
            },
            bases=(models.Model, imageboard.models.DateMixin),
        ),
        migrations.CreateModel(
            name='UserPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_number', models.PositiveIntegerField(default=imageboard.models.UserPost.get_post_number, unique=True)),
                ('name', models.CharField(default='Anonymous', max_length=20)),
                ('time_made', models.DateTimeField(auto_now=True)),
                ('post', models.CharField(max_length=5000)),
                ('ip_address', models.GenericIPAddressField()),
                ('thread', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='imageboard.Thread')),
            ],
            options={
                'ordering': ['post_number'],
            },
            bases=(models.Model, imageboard.models.DateMixin),
        ),
    ]
