# Generated by Django 4.2.2 on 2023-09-13 09:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0071_alter_resume_job'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resume',
            name='job',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='backend.job', verbose_name='Ваканция'),
            preserve_default=False,
        ),
    ]
