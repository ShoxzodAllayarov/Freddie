# Generated by Django 3.2.7 on 2022-02-16 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0012_auto_20220216_2234'),
    ]

    operations = [
        migrations.AddField(
            model_name='parser',
            name='link_from_chanel',
            field=models.CharField(default=2, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='parser',
            name='from_chanels_chat_id',
            field=models.IntegerField(default=0, verbose_name='Донор чат'),
        ),
    ]
