# Generated by Django 2.1 on 2018-08-13 21:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0009_auto_20180813_2323'),
        ('utils', '0003_genre'),
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stage_name', models.CharField(max_length=50, verbose_name='Stage name')),
                ('alias', models.CharField(blank=True, max_length=50, null=True, verbose_name='aka')),
                ('bio', models.TextField(verbose_name='Artist Bio')),
                ('dob', models.DateField(blank=True, null=True, verbose_name="Artist's date of birth")),
                ('genre', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='artist_genre', to='utils.Genre')),
                ('user_profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='account.Profile', verbose_name='User Profile')),
            ],
            options={
                'verbose_name': 'Artist Profile',
                'verbose_name_plural': 'Artists',
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person', models.CharField(max_length=50, verbose_name='Contact Person')),
                ('purpose', models.CharField(max_length=50, verbose_name='')),
                ('phone', models.CharField(max_length=50, verbose_name="Contact Person's Phone")),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name="Contact Person's Email Address")),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='artists.Artist', verbose_name='Artist')),
            ],
            options={
                'verbose_name': 'Contact',
                'verbose_name_plural': 'Artist Contacts',
            },
        ),
    ]
