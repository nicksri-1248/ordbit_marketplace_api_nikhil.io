# Generated by Django 4.2.2 on 2023-06-11 07:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0006_order_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='address_line_1',
        ),
        migrations.RemoveField(
            model_name='order',
            name='address_line_2',
        ),
        migrations.RemoveField(
            model_name='order',
            name='city',
        ),
        migrations.RemoveField(
            model_name='order',
            name='state',
        ),
        migrations.RemoveField(
            model_name='order',
            name='zip_code',
        ),
    ]