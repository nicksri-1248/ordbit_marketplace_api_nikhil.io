# Generated by Django 4.2.2 on 2023-06-11 04:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0004_order_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='user',
        ),
    ]
