# Generated by Django 2.2.9 on 2021-01-21 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0006_auto_20201229_1359'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='downloadable_file',
            field=models.FileField(blank=True, null=True, upload_to='books'),
        ),
    ]
