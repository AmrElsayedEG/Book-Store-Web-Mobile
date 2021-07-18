from django.shortcuts import get_object_or_404
from orders.models import order
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver
from paypal.standard.models import ST_PP_COMPLETED
from payment.models import Payment
from django.utils.timezone import now


#@receiver(valid_ipn_received)
def payment_notification(sender, **kwargs):
    ipn = sender
    if ipn.payment_status == ST_PP_COMPLETED:
        # payment was successful
        o = get_object_or_404(order, id=int(ipn.invoice))

        if int(round(float(o.usd_amount), 2)) == int(ipn.mc_gross):
            # mark the order as paid
            o.is_paid = True
            o.payment_method = 'PayPal'
            #Payment(user=o.user, payment_method="PayPal", order_id=o.id, cost=o.get_total_cost(), date=now()).save()
            o.save()
valid_ipn_received.connect(payment_notification)
