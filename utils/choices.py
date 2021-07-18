# list of all choices
from django.db import models
from django.utils.translation import gettext_lazy as _


class CountryListChoices(models.TextChoices):
    EGYPT = 'Egypt', _('Egypt')

class PaymentChoices(models.TextChoices):
    PAYPAL = 'PayPal', _('PayPal')
    ON_DEL = 'On Delivery', _('On Delivery')

class OrderStatusChoices(models.TextChoices):
    WAITING = 'Waiting', _('Waiting')
    Delivering = 'Delivering', _('Delivering')
    Delivered = 'Delivered', _('Delivered')
    Canceled = 'Canceled', _('Canceled')

class YesNoChoices(models.IntegerChoices):
    YES = 1, _('Yes')
    NO = 2, _('No')