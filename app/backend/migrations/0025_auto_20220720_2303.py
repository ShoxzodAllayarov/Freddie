# Generated by Django 3.2.3 on 2022-07-20 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0024_alter_parser_pause'),
    ]

    operations = [
        migrations.AddField(
            model_name='parser',
            name='ex_link',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='ссылки исключения'),
        ),
        migrations.AlterField(
            model_name='parser',
            name='pause',
            field=models.CharField(default='0', max_length=255, verbose_name='Пауза'),
        ),
    ]