# Generated by Django 4.2.2 on 2023-06-23 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0052_rename_user_answers_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='users',
            field=models.ManyToManyField(to='backend.botuser', verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='test',
            name='photo',
            field=models.FileField(blank=True, null=True, upload_to='', verbose_name='Фото'),
        ),
    ]