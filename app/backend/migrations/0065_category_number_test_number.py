# Generated by Django 4.2.2 on 2023-07-15 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0064_ads_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='number',
            field=models.IntegerField(default=0, verbose_name='Порядочный номер'),
        ),
        migrations.AddField(
            model_name='test',
            name='number',
            field=models.IntegerField(default=0, verbose_name='Порядочный номер'),
        ),
    ]
