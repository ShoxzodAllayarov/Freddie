# Generated by Django 3.2.3 on 2022-07-20 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0023_parser_pause'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parser',
            name='pause',
            field=models.CharField(default='0', max_length=255),
        ),
    ]
