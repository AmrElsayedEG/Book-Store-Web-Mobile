# Generated by Django 2.2.9 on 2020-12-29 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0005_auto_20201229_1355'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='pages',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='release_year',
            field=models.CharField(default='2021', max_length=5),
        ),
    ]
