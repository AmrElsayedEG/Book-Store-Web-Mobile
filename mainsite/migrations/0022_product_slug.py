# Generated by Django 2.2.9 on 2021-03-27 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0021_author_born'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(max_length=250, null=True, unique=True),
        ),
    ]
