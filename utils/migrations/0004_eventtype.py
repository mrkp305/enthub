# Generated by Django 2.1 on 2018-08-15 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0003_genre'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Event Type')),
            ],
            options={
                'verbose_name': 'Event type',
                'verbose_name_plural': 'Event types',
            },
        ),
    ]
