# Generated by Django 2.2.9 on 2021-03-25 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0018_coupon_discount_percentage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='downloadable_file',
        ),
        migrations.RemoveField(
            model_name='product',
            name='ebook',
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(max_length=10000),
        ),
    ]