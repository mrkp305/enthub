# Generated by Django 2.1 on 2018-08-14 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artists', '0007_remove_artist_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='purpose',
            field=models.CharField(max_length=50, verbose_name='Purpose Of The Contact'),
        ),
    ]
