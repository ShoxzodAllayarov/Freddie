# Generated by Django 3.2.7 on 2022-02-01 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0008_alter_parser_to_chanel_chat_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parser',
            name='from_chanels_chat_id',
            field=models.IntegerField(verbose_name='Донор Каналы'),
        ),
    ]