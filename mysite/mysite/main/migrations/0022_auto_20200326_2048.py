# Generated by Django 2.2 on 2020-03-26 12:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_merge_20200326_2047'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parent',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='user',
            name='phone',
        ),
    ]