from django.db import models
from utils import YesNoChoices
from django.template.defaultfilters import slugify
# Create your models here.

class website_layout(models.Model):
    logo_dark = models.ImageField(upload_to='website_layout',default='website-layout/default.jpg')
    logo_light = models.ImageField(upload_to='website_layout',default='website-layout/default.jpg')
    facebook = models.URLField(max_length=200, null=True, blank=True)
    twitter = models.URLField(max_length=200, null=True, blank=True)
    instagram = models.URLField(max_length=200, null=True, blank=True)
    


class Category(models.Model):
    category_name = models.CharField(max_length=20)
    category_image = models.ImageField(upload_to='cat-imgs',default='book-imgs/default.jpg')
    def __str__(self):
        return self.category_name

class author(models.Model):
    author_name = models.CharField(max_length=30)
    author_picture = models.ImageField(upload_to='author-imgs',default='book-imgs/default.jpg')
    about_author = models.TextField(max_length=500,default="Author Details")
    author_nationality = models.CharField(max_length=30, default="Egyptian")
    born = models.IntegerField(default=2000)
    def __str__(self):
        return self.author_name

class publisher(models.Model):
    publisher_name = models.CharField(max_length=30)
    publisher_picture = models.ImageField(upload_to='publisher-imgs',default='book-imgs/default.jpg')
    about_publisher = models.TextField(max_length=500)
    def __str__(self):
        return self.publisher_name

class Product(models.Model):
    
    title = models.CharField(max_length=100)
    release_year = models.CharField(max_length=5,default="2021")
    pages = models.IntegerField(default=0)
    description = models.TextField(max_length=10000)
    weight = models.DecimalField(max_digits=10,decimal_places=2)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    discount_price = models.DecimalField(max_digits=10,decimal_places=2, null=True,blank=True)
    publisher = models.ForeignKey(publisher, on_delete=models.CASCADE, null=True,blank=True)
    author = models.ForeignKey(author, on_delete=models.CASCADE, null=True,blank=True, related_name='author')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True, blank=True)
    main_image = models.ImageField(upload_to='book-imgs',default='book-imgs/default.jpg')
    is_product_live = models.SmallIntegerField(choices=YesNoChoices.choices, default=YesNoChoices.YES)
    in_stock_number = models.IntegerField(default=0)
    advertising_banner = models.SmallIntegerField(choices=YesNoChoices.choices, default=YesNoChoices.NO)
    ordered_times = models.IntegerField(default=0)
    slug = models.SlugField(max_length = 250, blank=True, null=True, unique=True)

    def save(self, *args, **kwargs):
        if self.advertising_banner == 1:
            try:
                temp = Product.objects.get(advertising_banner=1)
                if self != temp:
                    temp.advertising_banner = 2
                    temp.save()
            except Product.DoesNotExist:
                pass
        if not self.slug:
            string = "%s-%s-%s" % (self.title, self.author, self.id)
            self.slug = slugify(string)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class coupon(models.Model):
    
    code = models.CharField(max_length=10)
    discount_percentage = models.IntegerField(default=0)
    active = models.BooleanField(choices=YesNoChoices.choices,default=YesNoChoices.YES)

    def __str__(self):
        return '{} - {}'.format(self.code,self.active)

class shipping_fee(models.Model):
    city = models.CharField(max_length=20, unique=True)
    fees = models.IntegerField(default=0)

    def __str__(self):
        return '{} -> {} EGP'.format(self.city,str(self.fees))
