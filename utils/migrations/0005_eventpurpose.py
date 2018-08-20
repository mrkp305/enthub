# Generated by Django 2.1 on 2018-08-20 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0004_eventtype'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventPurpose',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purpose', models.CharField(max_length=50, verbose_name='Purpose')),
            ],
            options={
                'verbose_name': 'Purpose',
                'verbose_name_plural': 'Venue Purposes',
            },
        ),
    ]
