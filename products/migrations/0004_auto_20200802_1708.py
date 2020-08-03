# Generated by Django 3.0.8 on 2020-08-02 11:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20200802_1701'),
    ]

    operations = [
        migrations.AddField(
            model_name='box',
            name='creation_date',
            field=models.DateField(default=datetime.date(2020, 8, 2)),
        ),
        migrations.AlterField(
            model_name='box',
            name='area',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='box',
            name='created_by',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='box',
            name='height',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='box',
            name='last_updated_date',
            field=models.DateField(default=datetime.date(2020, 8, 2)),
        ),
        migrations.AlterField(
            model_name='box',
            name='length',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='box',
            name='user_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='box',
            name='volume',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='box',
            name='width',
            field=models.IntegerField(default=0),
        ),
    ]
