# Generated by Django 5.1.2 on 2024-12-13 20:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WatchingHub', '0015_alter_settings_sort_shows_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='Filter_By_Classification',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='filtered_shows', to='WatchingHub.classification'),
        ),
    ]
