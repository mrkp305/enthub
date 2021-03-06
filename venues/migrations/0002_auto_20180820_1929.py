# Generated by Django 2.1 on 2018-08-20 19:29

from django.db import migrations, models
import django.db.models.deletion
import venues.models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0005_eventpurpose'),
        ('venues', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=venues.models.directory_path, verbose_name='Venue Image')),
                ('is_main', models.BooleanField(default=False, verbose_name='Is main banner')),
            ],
        ),
        migrations.AddField(
            model_name='venue',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='utils.City', verbose_name='City'),
        ),
        migrations.AddField(
            model_name='venue',
            name='contact_person',
            field=models.CharField(default='KL', max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='venue',
            name='description',
            field=models.TextField(default='k', verbose_name='Description'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='venue',
            name='email',
            field=models.EmailField(default='me@me.com', max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='venue',
            name='is_on_whatsapp',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='venue',
            name='latitude',
            field=models.CharField(default='987', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='venue',
            name='longitude',
            field=models.CharField(default='kjh', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='venue',
            name='name',
            field=models.CharField(default='Hehe', max_length=150),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='venue',
            name='phone',
            field=models.CharField(default='987', max_length=15),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='venue',
            name='street_address',
            field=models.CharField(default='sd', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='venue',
            name='suitable',
            field=models.ManyToManyField(blank=True, null=True, to='utils.EventPurpose', verbose_name='Suitable for'),
        ),
        migrations.AddField(
            model_name='venue',
            name='website',
            field=models.URLField(default='http://www.kd.com'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='images',
            name='venue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='venues.Venue', verbose_name='Venue'),
        ),
    ]
