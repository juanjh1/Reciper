# Generated by Django 4.2.9 on 2024-02-08 18:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2024, 2, 8, 18, 23, 5, 277793, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
    ]