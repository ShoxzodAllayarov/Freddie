# Generated by Django 4.2.2 on 2023-10-03 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0082_alter_category_options_botuser_delivery'),
    ]

    operations = [
        migrations.AddField(
            model_name='botuser',
            name='info',
            field=models.TextField(blank=True, null=True, verbose_name='Инфо'),
        ),
    ]
