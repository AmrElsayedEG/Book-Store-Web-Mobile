# Generated by Django 2.2.9 on 2021-03-15 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0017_auto_20210315_1138'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='discount_percentage',
            field=models.IntegerField(default=0),
        ),
    ]
