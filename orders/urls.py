from django.urls import re_path, path
from . import views
from orders.shipping_check import get_shipping_fees

app_name = 'orders'
urlpatterns = [
    re_path(r'^create/$',views.order_create,name='order'),
    path('check/coupon', views.coupon_req, name='check-coupon'),
    path('get/fees', get_shipping_fees, name='get-fees'),
]
