# Generated by Django 3.1.6 on 2023-01-10 19:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0032_auto_20230111_0054'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='botuser',
            options={'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.AlterModelOptions(
            name='buttons',
            options={'verbose_name': 'Кнопка', 'verbose_name_plural': 'кнопки'},
        ),
        migrations.AlterModelOptions(
            name='templates',
            options={'verbose_name': 'Шаблон', 'verbose_name_plural': 'Шаблоны'},
        ),
    ]
