# Generated by Django 2.1 on 2018-08-14 01:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('artists', '0006_contact_last_updated'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artist',
            name='avatar',
        ),
    ]