# Generated by Django 3.1.6 on 2023-01-10 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0034_auto_20230111_0149'),
    ]

    operations = [
        migrations.AddField(
            model_name='button',
            name='chat_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='command',
            name='chat_id',
            field=models.IntegerField(default=3),
            preserve_default=False,
        ),
    ]
