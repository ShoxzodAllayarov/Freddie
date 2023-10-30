# Generated by Django 4.2.2 on 2023-07-06 06:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0058_alter_acceptedtest_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ads',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст')),
                ('photo', models.FileField(blank=True, null=True, upload_to='', verbose_name='Фото')),
                ('count', models.IntegerField(verbose_name='')),
                ('sex', models.CharField(choices=[('All', 'Все'), ('Male', 'Мужской'), ('Female', 'Женский')], default='Male', max_length=255, verbose_name='Пол')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата регистрации')),
            ],
        ),
    ]