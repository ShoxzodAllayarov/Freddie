# Generated by Django 3.2.5 on 2021-11-15 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_botuser_keyboard_style'),
    ]

    operations = [
        migrations.AddField(
            model_name='botuser',
            name='language',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
