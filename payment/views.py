from django.shortcuts import render,get_object_or_404
from decimal import Decimal
from django.conf import settings
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from orders.models import order
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
from api.hash import encode,decode
import requests
from django.shortcuts import redirect
# Create your views here.


@csrf_exempt
def payment_done(request):
    if request.session.get('order_id'):
        del request.session['order_id']
        return render(request, 'done.html')
    else:
        return render(request,'canceled.html')



@csrf_exempt
def payment_canceled(request):
	return render(request,'canceled.html')


#
# def payment_process(request):
#     order_id = request.session.get('order_id')
#     orders = get_object_or_404(order, id=order_id)
#     host = request.get_host()
#     r = requests.get('https://openexchangerates.org/api/latest.json?app_id=673d60f0bb044fb8b42f2684f7c370ca&symbol=EGP').json()
#     usd_egp = r['rates']['EGP']
#     usd_amount = int(orders.get_total_cost()) / usd_egp
#     orders.usd_amount = usd_amount
#     orders.save()
#
#     paypal_dict = {
#         'business': settings.PAYPAL_RECEIVER_EMAIL,
#         'amount': '%.2f' % usd_amount,
#         'item_name': 'Order {}'.format(order.id),
#         'invoice': str(orders.id),
#         'currency_code': 'USD',
#         'notify_url': 'http://{}{}'.format(host,reverse('paypal-ipn')),
#         'return_url': 'http://{}{}'.format(host, reverse('payment:done')),
#         'cancel_return': 'http://{}{}'.format(host, reverse('payment:canceled')),
#     }
#
#     form = PayPalPaymentsForm(initial=paypal_dict)
#
#     context = {
#         'order': orders,
#         'form': form,
#     }
#     return render(request, 'process.html', context)



def payment_process(request, id):
    orders = get_object_or_404(order, id=id)
    print(orders.user.id, request.user.id, orders.payment_method, orders.is_paid)
    if orders.user.id == request.user.id and orders.is_paid is False:
        if not request.session.get('order_id'):
            request.session['order_id'] = orders.id
        host = request.get_host()
        r = requests.get('https://openexchangerates.org/api/latest.json?app_id=673d60f0bb044fb8b42f2684f7c370ca&symbol=EGP').json()
        usd_egp = r['rates']['EGP']
        usd_amount = int(orders.get_total_cost()) / usd_egp
        orders.usd_amount = usd_amount
        orders.save()

        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': '%.2f' % usd_amount,
            'item_name': 'Order {}'.format(order.id),
            'invoice': str(orders.id),
            'currency_code': 'USD',
            'notify_url': 'http://{}{}'.format(host,reverse('paypal-ipn')),
            'return_url': 'http://{}{}'.format(host, reverse('payment:done')),
            'cancel_return': 'http://{}{}'.format(host, reverse('payment:canceled')),
        }

        form = PayPalPaymentsForm(initial=paypal_dict)
        context = {
            'order': orders,
            'form': form,
            'usd_egp' : usd_egp,
            'usd_amount' : usd_amount,
        }
        return render(request, 'process.html', context)

    return redirect('/404/')


def mobile_payment_process(request,sec_key):
    original = decode(str(sec_key))
    data = original.split('---')
    token = Token.objects.get(key=data[0])
    user = token.user
    login(request, user)
    orders = get_object_or_404(order, id=data[1])
    print(orders.user.id, request.user.id, orders.payment_method, orders.is_paid)
    if orders.user.id == request.user.id and orders.is_paid is False:
        if not request.session.get('order_id'):
            request.session['order_id'] = orders.id
        host = request.get_host()
        r = requests.get('https://openexchangerates.org/api/latest.json?app_id=673d60f0bb044fb8b42f2684f7c370ca&symbol=EGP').json()
        usd_egp = r['rates']['EGP']
        usd_amount = int(orders.get_total_cost()) / usd_egp
        orders.usd_amount = usd_amount
        orders.save()

        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': '%.2f' % usd_amount,
            'item_name': 'Order {}'.format(data[1]),
            'invoice': str(data[1]),
            'currency_code': 'USD',
            'notify_url': 'http://{}{}'.format(host,reverse('paypal-ipn')),
            'return_url': 'http://{}{}'.format(host, reverse('payment:done')),
            'cancel_return': 'http://{}{}'.format(host, reverse('payment:canceled')),
        }

        form = PayPalPaymentsForm(initial=paypal_dict)

        context = {
            'order': orders,
            'form': form,
            'usd_egp' : usd_egp,
            'usd_amount' : usd_amount,
        }
        return render(request, 'process.html', context)
    return redirect('/404/')

def on_devlivery(request):
    return render(request,'on_delivery.html')
