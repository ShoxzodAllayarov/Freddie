# Generated by Django 3.2.3 on 2022-07-18 11:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0015_subchats'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SubChats',
            new_name='SubChat',
        ),
    ]
