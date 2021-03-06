# Generated by Django 2.1 on 2018-08-11 13:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('utils', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('handle', models.CharField(max_length=20, null=True, unique=True, verbose_name='Unique username')),
                ('phone', models.CharField(max_length=15, null=True, verbose_name='User phone number')),
                ('email_confirmed', models.BooleanField(default=False, verbose_name='Confirmation status')),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='utils.City')),
                ('tags', models.ManyToManyField(null=True, to='utils.Tag', verbose_name='User tags')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Credentials')),
            ],
        ),
    ]
