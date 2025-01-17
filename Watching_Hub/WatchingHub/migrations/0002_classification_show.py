# Generated by Django 5.1.2 on 2024-11-19 15:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WatchingHub', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Classification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Classification_Owner', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('Classification', models.CharField(max_length=64)),
                
            ],
        ),
        migrations.CreateModel(
            name='Show',
            fields=[
                ('Show_Owner', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Show_title', models.CharField(max_length=64)),
                ('Show_img', models.URLField()),
                ('Show_discription', models.TextField(blank=True)),
                ('Show_raring', models.FloatField(blank=True)),
                ('Date_finished_watching', models.DateTimeField(blank=True)),
                ('Publication_year', models.IntegerField(blank=True, max_length=4)),
                ('duration', models.DurationField(blank=True, null=True)),
                ('Show_Classification', models.ManyToManyField(to='WatchingHub.classification')),
                
            ],
        ),
    ]
