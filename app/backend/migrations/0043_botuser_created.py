# Generated by Django 3.1.6 on 2023-06-03 05:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0042_botuser_tests'),
    ]

    operations = [
        migrations.AddField(
            model_name='botuser',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата регистрации'),
        ),
    ]