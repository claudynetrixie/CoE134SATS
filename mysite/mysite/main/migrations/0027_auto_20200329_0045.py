# Generated by Django 2.2 on 2020-03-28 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_remove_contact_message_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact_message',
            name='message',
            field=models.TextField(),
        ),
    ]
