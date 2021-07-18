from urllib import request
from mainsite.models import Product, coupon
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from mainsite.models import shipping_fee
from django.utils.timezone import now
from payment.models import Payment
from utils import CountryListChoices, PaymentChoices, OrderStatusChoices
# Create your models here.

class order(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_orders')
    customer_name = models.CharField(max_length=50)
    address_1 = models.CharField(max_length=100)
    address_2 = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=6)
    city = models.CharField(max_length=50)
    country = models.CharField(choices=CountryListChoices.choices,max_length=50,default=CountryListChoices.EGYPT,blank=False)
    phone = models.CharField(max_length=15)
    notes = models.TextField(blank=True,null=True)
    coupon = models.ForeignKey(coupon, on_delete=models.SET_NULL, blank=True, null=True)
    payment_method = models.CharField(max_length=50,choices=PaymentChoices.choices,default=PaymentChoices.ON_DEL, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    order_status = models.CharField(max_length=50,choices=OrderStatusChoices.choices,default=OrderStatusChoices.WAITING,blank=False)
    usd_amount = models.FloatField(blank=True, null=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = "order"
        verbose_name_plural = "orders"
    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        total = sum(item.get_cost() for item in self.orderitems.all())
        if self.coupon:
            total -= (total * self.coupon.discount_percentage) / 100
        shipping = shipping_fee.objects.filter(city__iexact=self.city)
        if shipping.exists():
            shipping=shipping.last()
            total += shipping.fees
        else:
            shipping = shipping_fee.objects.get(city='default')
            total += shipping.fees
        return total

    total_price = property(get_total_cost)

    @property
    def used_coupon(self):
        if self.coupon:
            return 'Yes'
        return 'No'

    @property
    def get_shipping_fees(self):
        shipping = shipping_fee.objects.filter(city__iexact=self.city)
        if shipping.exists():
            shipping=shipping.last()
            return shipping.fees
        else:
            shipping = shipping_fee.objects.get(city='default')
            return shipping.fees

    def save(self, *args, **kwargs):
        if self.order_status == 'Delivering':
            if self.phone[:2] == "+2":
                phone_no = self.phone
            elif self.phone[:2] == "20":
                phone_no = "{}{}".format("+",self.phone)
            elif self.phone[:2] == "01":
                phone_no =  "{}{}".format("+2",self.phone)
            else:
                phone_no = None
            if not phone_no is None:
                import requests
                url = "https://http-api.d7networks.com/send"
                querystring = {
                    "username": "vdfk3526",
                    "password": "CZuXkp8J",
                    "from": "Test%20SMS",
                    "content": "Congrats, Your order is being delivered to you, Total {} EGP".format(self.get_total_cost()),
                    "dlr-method": "POST",
                    "dlr-url": "https://4ba60af1.ngrok.io/receive",
                    "dlr": "yes",
                    "dlr-level": "3",
                    "to": phone_no
                }
                headers = {
                    'cache-control': "no-cache"
                }
                requests.request("GET", url, headers=headers, params=querystring)

        if self.is_paid is True:
            m = Payment.objects.filter(order_id=self.id)
            if not m.exists():
                Payment(user=self.user,
                        order_id=self.id,
                         payment_method= self.payment_method,
                         cost=self.get_total_cost(),
                         date=now()).save()
            m = m.last()
            m.payment_method = self.payment_method
            m.save()
        super(order, self).save(*args, **kwargs)

class OrderItem(models.Model):
    order = models.ForeignKey(order,related_name='orderitems',on_delete=models.CASCADE)
    product = models.ForeignKey(Product,related_name='order_items',on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)


    class Meta:
        verbose_name = "OrderItem"
        verbose_name_plural = "OrderItems"

    def __str__(self):
        return '{}'.format(self.id)
    def get_cost(self):
        return self.price * self.quantity


def update_ordered_times(sender, **kwargs):
        instance = kwargs['instance']
        created = kwargs['created']
        raw = kwargs['raw']
        if created and not raw:
            instance.product.ordered_times += instance.quantity
            instance.product.in_stock_number -= instance.quantity
            if instance.product.in_stock_number <= 0:
                instance.product.is_product_live = 2
            instance.product.save()
post_save.connect(update_ordered_times, sender=OrderItem)
