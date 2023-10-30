# Generated by Django 4.2.2 on 2023-10-02 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0079_remove_shopcard_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='link',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Ссылка на товар'),
        ),
        migrations.AlterField(
            model_name='shopcard',
            name='count',
            field=models.IntegerField(default=0, verbose_name='Кол-ва'),
        ),
    ]
