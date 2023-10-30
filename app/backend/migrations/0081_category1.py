# Generated by Django 4.2.2 on 2023-10-03 02:07

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0080_product_link_alter_shopcard_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Названия')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата регистрации')),
                ('parent', models.ManyToManyField(to='backend.product', verbose_name='Товары')),
            ],
            options={
                'verbose_name_plural': 'категории',
            },
        ),
    ]