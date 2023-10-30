# Generated by Django 4.2.2 on 2023-10-15 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0092_alter_purchase_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='status',
            field=models.CharField(choices=[('Ожидания', 'Ожидания'), ('Подтвержден', 'Подтвержден'), ('Отклонен', 'Отклонен')], default='Ожидания', max_length=255, verbose_name='Статус оплаты'),
        ),
    ]