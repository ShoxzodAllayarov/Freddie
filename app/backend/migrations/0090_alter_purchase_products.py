# Generated by Django 4.2.2 on 2023-10-14 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0089_shopcard_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='products',
            field=models.ManyToManyField(blank=True, to='backend.shopcard', verbose_name='Продукты'),
        ),
    ]
