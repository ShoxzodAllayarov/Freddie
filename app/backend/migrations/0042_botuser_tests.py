# Generated by Django 3.1.6 on 2023-06-03 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0041_auto_20230603_0244'),
    ]

    operations = [
        migrations.AddField(
            model_name='botuser',
            name='tests',
            field=models.TextField(blank=True, default='', null=True, verbose_name='Айди пройденных тестов(тест-ответ)'),
        ),
    ]
