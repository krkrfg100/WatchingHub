# Generated by Django 5.1.2 on 2024-11-20 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WatchingHub', '0004_alter_show_show_classification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='show',
            name='Show_Classification',
            field=models.ManyToManyField(related_name='shows', to='WatchingHub.classification'),
        ),
    ]
