# Generated by Django 2.2.9 on 2021-04-27 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_auto_20210427_2051'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='order_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
