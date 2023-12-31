# Generated by Django 4.2.2 on 2023-10-02 21:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0077_remove_product_image_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(verbose_name='Кол-ва')),
                ('status', models.BooleanField(default=False, verbose_name='Куплено')),
                ('price_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.priceandtitle', verbose_name='Товар')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.botuser', verbose_name='пользователь')),
            ],
        ),
    ]
