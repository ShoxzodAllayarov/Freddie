# Generated by Django 3.2.3 on 2022-07-19 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0018_parser_notlink'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parser',
            name='from_chanels_chat_id',
            field=models.IntegerField(verbose_name='Донор чат'),
        ),
        migrations.AlterField(
            model_name='parser',
            name='keywords',
            field=models.TextField(null=True, verbose_name='Ключевые слова'),
        ),
    ]
