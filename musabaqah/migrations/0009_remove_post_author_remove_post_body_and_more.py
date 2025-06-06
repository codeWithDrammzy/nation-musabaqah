# Generated by Django 5.1.7 on 2025-05-04 15:24

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musabaqah', '0008_alter_stateuser_password_post'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='author',
        ),
        migrations.RemoveField(
            model_name='post',
            name='body',
        ),
        migrations.RemoveField(
            model_name='post',
            name='image',
        ),
        migrations.RemoveField(
            model_name='post',
            name='video',
        ),
        migrations.AddField(
            model_name='post',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='post',
            name='media',
            field=models.FileField(blank=True, null=True, upload_to='posts/'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='stateuser',
            name='password',
            field=models.CharField(default='pbkdf2_sha256$870000$iGbNB7YkubIxCCEPnkJZBs$FMG2yDm3ClskAeSSmAXzgGYkuh395bltNJS2edSzyLw=', max_length=128),
        ),
    ]
