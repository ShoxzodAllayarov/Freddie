# Generated by Django 4.2.2 on 2023-09-13 09:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0069_alter_resume_job'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resume',
            name='job',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='backend.job', verbose_name='Ваканция'),
        ),
        migrations.AlterField(
            model_name='resume',
            name='text',
            field=models.TextField(blank=True, null=True, verbose_name='описания'),
        ),
    ]
