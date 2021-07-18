# Generated by Django 2.2.9 on 2021-03-15 11:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0018_coupon_discount_percentage'),
        ('orders', '0007_remove_order_auto_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='coupon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mainsite.coupon'),
        ),
    ]
