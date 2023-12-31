# Generated by Django 4.2.2 on 2023-06-22 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0049_alter_answers_options_alter_question_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='answers',
            name='user',
            field=models.ManyToManyField(to='backend.botuser', verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='botuser',
            name='tests',
            field=models.TextField(blank=True, default='', null=True, verbose_name='Айди пройденных тестов(ответ)'),
        ),
    ]
