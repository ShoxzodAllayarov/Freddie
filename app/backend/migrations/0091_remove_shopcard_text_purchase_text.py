# Generated by Django 4.2.2 on 2023-10-14 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0090_alter_purchase_products'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shopcard',
            name='text',
        ),
        migrations.AddField(
            model_name='purchase',
            name='text',
            field=models.TextField(default=1, verbose_name='тест'),
            preserve_default=False,
        ),
    ]