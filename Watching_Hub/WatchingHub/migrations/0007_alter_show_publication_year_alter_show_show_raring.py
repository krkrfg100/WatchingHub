# Generated by Django 5.1.2 on 2024-11-23 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WatchingHub', '0006_alter_show_date_finished_watching_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='show',
            name='Publication_year',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='show',
            name='Show_raring',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
    ]
