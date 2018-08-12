# Generated by Django 2.1 on 2018-08-11 13:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20180811_1546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='utils.City'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='handle',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='Unique username'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='User phone number'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='utils.Tag', verbose_name='User tags'),
        ),
    ]