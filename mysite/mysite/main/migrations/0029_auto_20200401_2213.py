# Generated by Django 2.2 on 2020-04-01 14:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0028_contact_message_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact_message',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 1, 22, 13, 32, 802801)),
        ),
    ]
