# Generated by Django 3.1.6 on 2023-01-17 16:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0037_auto_20230116_1855'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='botuser',
            name='ans5',
        ),
    ]