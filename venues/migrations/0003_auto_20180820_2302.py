# Generated by Django 2.1 on 2018-08-20 23:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0002_auto_20180820_1929'),
    ]

    operations = [
        migrations.AddField(
            model_name='venue',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Last Updated On'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='venue',
            name='last_modified',
            field=models.DateTimeField(auto_now=True, verbose_name='Last Updated On'),
        ),
    ]
