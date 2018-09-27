# Generated by Django 2.0.6 on 2018-09-27 12:04

from django.db import migrations, models
import embed_video.fields


class Migration(migrations.Migration):

    dependencies = [
        ('imageboard', '0006_auto_20180923_1024'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='id_enabled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userpost',
            name='poster_id',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='thread',
            name='embed',
            field=embed_video.fields.EmbedVideoField(blank=True, help_text='Youtube, Vimeo or Soundcloud URL', null=True),
        ),
        migrations.AlterField(
            model_name='userpost',
            name='embed',
            field=embed_video.fields.EmbedVideoField(blank=True, help_text='Youtube, Vimeo or Soundcloud URL', null=True),
        ),
    ]
