# Generated by Django 2.2.9 on 2021-04-23 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0025_auto_20210402_2102'),
    ]

    operations = [
        migrations.CreateModel(
            name='shipping_fee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=20)),
                ('fees', models.IntegerField(default=0)),
            ],
        ),
        migrations.AlterField(
            model_name='product',
            name='advertising_banner',
            field=models.BooleanField(choices=[(0, 'No'), (1, 'Yes')], default=0),
        ),
    ]