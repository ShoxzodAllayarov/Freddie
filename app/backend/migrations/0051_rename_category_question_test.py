# Generated by Django 4.2.2 on 2023-06-22 06:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0050_answers_user_alter_botuser_tests'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='category',
            new_name='test',
        ),
    ]
