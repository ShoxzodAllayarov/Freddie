# Generated by Django 3.2.7 on 2022-01-31 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_botuser_language'),
    ]

    operations = [
        migrations.CreateModel(
            name='Parser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('to_chanel_chat_id', models.ImageField(upload_to='', verbose_name='Основной канал')),
                ('from_chanels_chat_id', models.TextField(verbose_name='Донор Каналы')),
                ('keywords', models.TextField(verbose_name='Ключевые слова')),
            ],
        ),
        migrations.DeleteModel(
            name='Music',
        ),
        migrations.RemoveField(
            model_name='botuser',
            name='keyboard_style',
        ),
        migrations.RemoveField(
            model_name='botuser',
            name='language',
        ),
        migrations.RemoveField(
            model_name='botuser',
            name='requests_count',
        ),
    ]