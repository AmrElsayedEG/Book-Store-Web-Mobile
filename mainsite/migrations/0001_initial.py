# Generated by Django 3.2 on 2021-07-18 13:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_name', models.CharField(max_length=30)),
                ('author_picture', models.ImageField(default='book-imgs/default.jpg', upload_to='author-imgs')),
                ('about_author', models.TextField(default='Author Details', max_length=500)),
                ('author_nationality', models.CharField(default='Egyptian', max_length=30)),
                ('born', models.IntegerField(default=2000)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=20)),
                ('category_image', models.ImageField(default='book-imgs/default.jpg', upload_to='cat-imgs')),
            ],
        ),
        migrations.CreateModel(
            name='coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10)),
                ('discount_percentage', models.IntegerField(default=0)),
                ('active', models.BooleanField(choices=[(1, 'Yes'), (2, 'No')], default=1)),
            ],
        ),
        migrations.CreateModel(
            name='publisher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publisher_name', models.CharField(max_length=30)),
                ('publisher_picture', models.ImageField(default='book-imgs/default.jpg', upload_to='publisher-imgs')),
                ('about_publisher', models.TextField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='shipping_fee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=20, unique=True)),
                ('fees', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='website_layout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo_dark', models.ImageField(default='website-layout/default.jpg', upload_to='website_layout')),
                ('logo_light', models.ImageField(default='website-layout/default.jpg', upload_to='website_layout')),
                ('facebook', models.URLField(blank=True, null=True)),
                ('twitter', models.URLField(blank=True, null=True)),
                ('instagram', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('release_year', models.CharField(default='2021', max_length=5)),
                ('pages', models.IntegerField(default=0)),
                ('description', models.TextField(max_length=10000)),
                ('weight', models.DecimalField(decimal_places=2, max_digits=10)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('discount_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('main_image', models.ImageField(default='book-imgs/default.jpg', upload_to='book-imgs')),
                ('is_product_live', models.SmallIntegerField(choices=[(1, 'Yes'), (2, 'No')], default=1)),
                ('in_stock_number', models.IntegerField(default=0)),
                ('advertising_banner', models.SmallIntegerField(choices=[(1, 'Yes'), (2, 'No')], default=2)),
                ('ordered_times', models.IntegerField(default=0)),
                ('slug', models.SlugField(blank=True, max_length=250, null=True, unique=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='author', to='mainsite.author')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainsite.category')),
                ('publisher', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainsite.publisher')),
            ],
        ),
    ]
