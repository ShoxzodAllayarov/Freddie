# Generated by Django 4.2.2 on 2023-06-24 06:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0054_alter_answers_users_alter_question_users_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_text', models.TextField(verbose_name='Текст')),
                ('sent', models.BooleanField(default=False, verbose_name='Отправлено')),
                ('datetime', models.DateTimeField(verbose_name='Дата рассылки')),
                ('paid_choice', models.CharField(blank=True, choices=[('male', 'Мужчины'), ('female', 'Женщины'), ('all', 'Всем')], default='all', max_length=20, null=True, verbose_name='Выбор получателей')),
                ('users_list', models.ManyToManyField(blank=True, to='backend.botuser', verbose_name='Список пользователей')),
            ],
            options={
                'verbose_name': 'рассылку',
                'verbose_name_plural': 'Рассылка',
            },
        ),
        migrations.CreateModel(
            name='Load',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_choice', models.CharField(choices=[('photo', 'Фото'), ('video', 'Видео'), ('document', 'Документ'), ('audio', 'Аудио')], default='photo', max_length=20, verbose_name='Выбор типа')),
                ('file', models.FileField(upload_to='media/', verbose_name='Файл')),
                ('mailing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='loads', to='backend.mailing')),
            ],
            options={
                'verbose_name': 'Файл',
                'verbose_name_plural': 'Файлы',
            },
        ),
    ]
