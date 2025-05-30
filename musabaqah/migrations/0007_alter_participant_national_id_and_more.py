# Generated by Django 5.1.7 on 2025-04-30 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musabaqah', '0006_alter_stateuser_password_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='national_id',
            field=models.CharField(max_length=11, unique=True),
        ),
        migrations.AlterField(
            model_name='stateuser',
            name='password',
            field=models.CharField(default='pbkdf2_sha256$870000$2JQysCUBmkkpqqrmuOCLST$gyP3+0zSWarC2TOzuvycThLxqf5w/FoLSQB9KHPEh5A=', max_length=128),
        ),
    ]
