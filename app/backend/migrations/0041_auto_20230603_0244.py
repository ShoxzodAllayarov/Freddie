# Generated by Django 3.1.6 on 2023-06-02 21:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0040_auto_20230602_2204'),
    ]

    operations = [
        migrations.RenameField(
            model_name='testcase',
            old_name='pont',
            new_name='point',
        ),
    ]
