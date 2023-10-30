# Generated by Django 4.2.2 on 2023-10-11 04:33

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0085_remove_mailing_message_text_eng'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailing',
            name='message_text_ru',
            field=models.TextField(verbose_name='Текст'),
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False, verbose_name='Статус оплаты')),
                ('payment_check', models.FileField(blank=True, null=True, upload_to='check', verbose_name='Чек')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата')),
                ('products', models.ManyToManyField(to='backend.shopcard', verbose_name='Продукты')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.botuser', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'заказ',
                'verbose_name_plural': 'заказы',
            },
        ),
    ]