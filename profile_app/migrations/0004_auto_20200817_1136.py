# Generated by Django 3.0.8 on 2020-08-17 02:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('profile_app', '0003_auto_20200812_1514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='birth',
            field=models.DateField(default=datetime.datetime(1992, 8, 17, 11, 36, 19, 631812), verbose_name='生年月日'),
        ),
    ]
