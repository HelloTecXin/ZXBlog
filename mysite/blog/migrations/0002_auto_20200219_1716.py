# Generated by Django 2.1.4 on 2020-02-19 09:16

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogarticles',
            name='publish',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 19, 9, 16, 3, 437957, tzinfo=utc)),
        ),
    ]