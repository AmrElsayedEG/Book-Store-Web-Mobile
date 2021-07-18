from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from .forms import OrderCreateForm
from .models import OrderItem, order
from . import models
from mainsite.models import coupon
from cart.cart import Cart
from django.forms.widgets import HiddenInput
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import json
from accounts.models import Profile
# Create your views here.


@login_required
def order_create(request):
    cart = Cart(request)
    profile = get_object_or_404(Profile, user=request.user)
    if request.session.get('d_i') is None:
        coupon_cont = 0
    else:
        coupon_cont = coupon.objects.get(id=request.session.get('d_i')).discount_percentage

    print(coupon_cont)
    if len(cart) > 0:
        r = request.user
        if 'country' in request.POST:
            form = OrderCreateForm(request.POST)
            if form.is_valid():
                order = form.save(commit=False)
                order.user = request.user
                try:
                    order.coupon_id = request.session.get('d_i')
                    del request.session['d_i']
                except:
                    pass
                    
                order.save()
                for item in cart:
                    OrderItem.objects.create(
                        order=order,
                        product=item['product'],
                        price=item['price'],
                        quantity=item['quantity'])

                cart.clear()
                context = {
                    'order': order,
                    'r': r
                }
                request.session['order_id'] = order.id
                try:
                    del request.session['total_cost']
                except:
                    pass
                order_info_email(order.id) #Send Email
                #Return to payment if on_delivery then return to dashboard
                if order.payment_method == "PayPal":
                    return redirect(reverse('payment:process', kwargs={'id':order.id}))
                else:
                    return redirect(reverse('payment:on_devlivery-payment'))
            #return render(request, 'created.html', context)
    else:
        return redirect(reverse('cart:cart_detail'))
    
    context = {
        'cart': cart,
        'r': r,
        'profile' : profile,
        'coupon_cont' : coupon_cont,
    }
    return render(request, 'Shipping-page.html', context)


def check_coupon(code,request):
    coupon_model = coupon.objects.filter(code=code)
    cart = Cart(request)

    if coupon_model.exists():
        coupon_model = coupon_model.first()
        if coupon_model.active == False:
            return {'status':'Coupon Code Expired'}
        else:
            prev = order.objects.filter(coupon=coupon_model,user_id=request.user)
            if prev.exists():
                return {'status':'You already used this coupon'}
            else:
                if request.session.get('total_cost') is None:
                    request.session['total_cost'] = cart.get_total_cost()
                price_after_discount = float(request.session.get('total_cost')) - float(((coupon_model.discount_percentage * cart.get_total_cost()) / 100))
                c_id = coupon_model.id
                request.session['total_cost'] = price_after_discount
                if not request.session.get('city_fees') is None:
                     price_after_discount += float(request.session.get('city_fees'))
                
                return {'status':'Coupon Added', 'new_price':price_after_discount, 'coupon_id':int(c_id)}
    else:
        return {'status':'Coupon Don\'t exist'}


def order_info_email(orderid):
    orders = order.objects.get(id=orderid)
    items = OrderItem.objects.filter(order=orders)
    subject = "Book Store - Order Submitted"
    email_template_name = "order-info.html"
    c = {
        "fullname" : orders.customer_name,
        "orders" : items,
        "totalprice" : orders.get_total_cost(),
        }
    email = render_to_string(email_template_name, c)
    msg = EmailMultiAlternatives(
                subject, 'Book Store', to=[orders.user.email]
            )
    msg.attach_alternative(email, "text/html")
    msg.send()
    
def coupon_req(request):
    ##### AJAX
    if request.method == 'POST' and request.is_ajax():
        check = check_coupon(request.POST['discount_code'], request)
        if check['status'] == 'Coupon Added':
            #cart.get_total_price = check['new_price']
            request.session['d_i'] = check['coupon_id']
            percentage = coupon.objects.get(id=check['coupon_id']).discount_percentage
            res = {'status' : 'Added', 'percentage' : percentage, 'new_price' : check['new_price']}
            return HttpResponse(json.dumps(res), content_type='application/json')
                    
        else:
            res = {'status' : 'Wrong'}
            return HttpResponse(json.dumps(res), content_type='application/json')
    #########
