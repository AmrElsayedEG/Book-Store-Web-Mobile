# Generated by Django 2.2.9 on 2021-03-25 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0019_auto_20210325_1106'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='author_nationality',
            field=models.CharField(default='Egyptian', max_length=30),
        ),
    ]
