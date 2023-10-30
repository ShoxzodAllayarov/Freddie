# Generated by Django 4.2.2 on 2023-07-06 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0061_alter_ads_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='ads',
            name='status',
            field=models.BooleanField(default=1, verbose_name='Статус'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ads',
            name='count',
            field=models.IntegerField(verbose_name='Кол-во показов'),
        ),
    ]
