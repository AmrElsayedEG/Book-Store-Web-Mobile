# Generated by Django 2.2.9 on 2021-04-27 16:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0013_order_payment_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='payment_date',
        ),
    ]
