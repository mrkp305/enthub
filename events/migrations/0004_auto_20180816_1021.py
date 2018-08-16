# Generated by Django 2.1 on 2018-08-16 08:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='admission',
            field=models.TextField(blank=True, null=True, verbose_name='Admission'),
        ),
        migrations.AlterField(
            model_name='location',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='utils.City', verbose_name=''),
        ),
    ]
