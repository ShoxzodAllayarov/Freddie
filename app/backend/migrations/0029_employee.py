# Generated by Django 3.2.3 on 2022-08-08 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0028_alter_report_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('username', models.CharField(max_length=255)),
            ],
        ),
    ]