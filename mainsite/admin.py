from django.contrib import admin
from .models import Category,author,Product, publisher, coupon, website_layout, shipping_fee
# Register your models here.

class CustomCategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name',)
    search_fields = ('category_name',)

class CustomAuthorAdmin(admin.ModelAdmin):
    list_display = ('author_name',)
    search_fields = ('author_name',)


class CustomProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_year', 'is_product_live', 'in_stock_number', 'ordered_times', 'advertising_banner',)
    search_fields = ('title', 'release_year',)
    list_filter = ('release_year','is_product_live', 'in_stock_number', 'ordered_times', 'advertising_banner',)

class CustomPublisherAdmin(admin.ModelAdmin):
    list_display = ('publisher_name',)
    search_fields = ('publisher_name',)

class CustomCouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percentage', 'active',)
    search_fields = ('active',)

admin.site.register(website_layout)
admin.site.register(Category, CustomCategoryAdmin)
admin.site.register(author, CustomAuthorAdmin)
admin.site.register(Product, CustomProductAdmin)
admin.site.register(publisher, CustomPublisherAdmin)
admin.site.register(coupon, CustomCouponAdmin)
admin.site.register(shipping_fee)
