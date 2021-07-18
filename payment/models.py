from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Payment(models.Model):
    PAY_TYPE = (
    	('PayPal','PayPal'),
    	('On Delivery','On Delivery'),
    	)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    order_id = models.PositiveIntegerField(blank=True, null=True)
    payment_method = models.CharField(max_length=30, choices=PAY_TYPE)
    cost = models.DecimalField(max_digits=20, decimal_places=2)
    date = models.DateTimeField(blank=True, null=True)

