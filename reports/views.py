from django.shortcuts import render
from orders.models import order
from payment.models import Payment
from mainsite.models import Product, publisher, author
from datetime import date
import datetime
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
# Create your views here.

@login_required
def export_report(request, type):
    if request.user.is_staff:
        res = HttpResponse(content_type='application/ms-excel')
        import pandas as pd
        if type == "payment":
            res['Content-Disposition'] = 'attachment; filename="payment-report.xls"'
            dataset = Payment.objects.all().order_by('-id')

            date = []
            amount = []
            type = []
            user = []

            for i in dataset:
                date.append(i.date.strftime("%Y-%m-%d"))
                amount.append(i.cost)
                type.append(i.payment_method)
                user.append(i.user.email)

            data = {"Date": date,
                    "Amount": amount,
                    "Type": type,
                    "User" : user,
                    }
            df = pd.DataFrame(data)
            df.to_excel(res, index=False)
            return res

        elif type == "order":
            res['Content-Disposition'] = 'attachment; filename="orders-report.xls"'
            dataset = order.objects.all().order_by('-id')

            order_num = []
            payment_method = []
            coupon = []
            cost = []
            date = []
            status = []
            paid = []
            user = []

            for i in dataset:
                date.append(i.created.strftime("%Y-%m-%d"))
                coupon.append("" if i.coupon is None else "{}{}".format(i.coupon.discount_percentage,"%"))
                order_num.append(i.id)
                cost.append(i.get_total_cost())
                payment_method.append(i.payment_method)
                status.append(i.order_status)
                paid.append("Yes" if i.is_paid else "NO")
                user.append(i.user.email)

            data = {"Order ID": order_num,
                    "Date": date,
                    "Status": status,
                    "Payment Method": payment_method,
                    "Coupon" : coupon,
                    "Total": cost,
                    "Paid": paid,
                    "User": user,
                    }
            df = pd.DataFrame(data)
            df.to_excel(res, index=False)
            return res
    return redirect("/")


# Order Methods
def statistics_per_month_order(queryset):
    months = ["01", "02","03","04","05","06","07","08","09","10","11","12"]
    today = date.today()
    data = []
    for i in months:
        data.append(queryset.objects.filter(created__month=i, created__year=today.year).count())
    return {"data" : data, "date" : months}

def statistics_filter_order(queryset, timeframe):
    if timeframe == 'Lweek':
        timeframe = 7
    elif timeframe == 'Lmonth':
        timeframe = 30
    timeframe = int(timeframe)
    today = date.today()
    end = today + datetime.timedelta(days=-timeframe)
    dates = []
    delta = today - end
    for i in range(delta.days + 1):
        dates.append(end + datetime.timedelta(days=i))

    data = []
    for i in dates:
        data.append(queryset.objects.filter(created__date=i).count())

    dates = []
    for i in range(delta.days + 1):
        x = end + datetime.timedelta(days=i)
        dates.append(x.strftime('%m/%d/%Y'))

    return {"date" : dates, "data" : data}

# Payment Methods
def statistics_filter_payment(queryset, timeframe):
    if timeframe == 'Lweek':
        timeframe = 7
    elif timeframe == 'Lmonth':
        timeframe = 30
    today = date.today()
    end = today + datetime.timedelta(days=-timeframe)
    dates = []
    delta = today - end
    for i in range(delta.days + 1):
        dates.append(end + datetime.timedelta(days=i))

    data = []
    for i in dates:
        from django.db import models
        from django.db.models.functions import Cast
        x = queryset.objects.filter(date__date=i).values('cost').annotate(cost_f=Cast('cost',output_field=models.FloatField()))
        count = 0
        for z in x:
            count += z['cost_f']
        data.append(count)

    dates = []
    for i in range(delta.days + 1):
        x = end + datetime.timedelta(days=i)
        dates.append(x.strftime('%m/%d/%Y'))

    return {"date" : dates, "data" : data}

def statistics_per_month_payment(queryset):
    months = [1,2,3,4,5,6,7,8,9,10,11,12]
    today = date.today()
    data = []
    for i in months:
        from django.db import models
        from django.db.models.functions import Cast
        x = queryset.objects.filter(date__month=i, date__year=today.year).values('cost').annotate(cost_f=Cast('cost',output_field=models.FloatField()))
        count = 0
        for z in x:
            count += z['cost_f']
        data.append(count)
        #data.append(queryset.objects.filter(date__month=i, date__year=today.year).count())
    return {"data" : data, "date" : months}

#################################
#### Page ######
################################

@login_required
def home(request):
    if request.user.is_staff:

        return render(request, 'home.html')

    return redirect("/")

@login_required
def products(request):
    if request.user.is_staff:

        all_prod = Product.objects.all().count()
        active_prod = Product.objects.filter(is_product_live=1).count()
        not_active_prod = Product.objects.filter(is_product_live=2).count()
        pub = publisher.objects.all().count()
        auth = author.objects.all().count()

        context = {
            "all_prod" : all_prod,
            "active_prod" : active_prod,
            "pub" : pub,
            "auth" : auth,
            "not_active_prod" : not_active_prod,
        }

        return render(request, 'product-stat.html', context)

    return redirect("/")

@login_required
def orders(request):
    if request.user.is_staff:
        today = date.today()

        if 'filter' in request.GET and request.GET.get('filter') != 'Tyear':
            statistics = statistics_filter_order(order, request.GET['filter'])
            filter_cursor = request.GET['filter']
        else:
            statistics = statistics_per_month_order(order)
            filter_cursor = 'Tyear'

        pending_orders = order.objects.filter(order_status="Waiting").count()
        delivering_orders = order.objects.filter(order_status="Delivering").count()
        delivered_orders = order.objects.filter(order_status="Delivered").count()
        cancelled_orders = order.objects.filter(order_status="Cancelled").count()
        all_orders = order.objects.all().count()
        today_orders = order.objects.filter(created__date=today).count()

        context = {
            "statistics" : statistics,
            "pending_orders" : pending_orders,
            "delivering_orders" : delivering_orders,
            "delivered_orders" : delivered_orders,
            "cancelled_orders" : cancelled_orders,
            "all_orders" : all_orders,
            "today_orders" : today_orders,
            "filter_cursor" : filter_cursor,
        }

        return render(request, 'order.html', context)

    return redirect("/")




@login_required
def payment(request):
    if request.user.is_staff:
        today = date.today()

        if 'filter' in request.GET and request.GET.get('filter') != 'Tyear':
            statistics = statistics_filter_payment(Payment, request.GET['filter'])
            filter_cursor = request.GET['filter']
        else:
            statistics = statistics_per_month_payment(Payment)
            filter_cursor = 'Tyear'

        payment_lifetime = Payment.objects.all().count()
        payment_lifetime_currency = Payment.objects.all().aggregate(Sum('cost'))
        payment_today = Payment.objects.filter(date__date=today).count()
        payment_today_currency = Payment.objects.filter(date__date=today).aggregate(Sum('cost'))
        online_payment_lifetime = Payment.objects.filter(payment_method="PayPal").count()
        online_payment_lifetime_currency = Payment.objects.filter(payment_method="PayPal").aggregate(Sum('cost'))
        online_payment_today = Payment.objects.filter(date__date=today, payment_method="PayPal").count()
        online_payment_today_currency = Payment.objects.filter(date__date=today, payment_method="PayPal").aggregate(Sum('cost'))
        on_delivery_lifetime = Payment.objects.filter(payment_method="On Delivery").count()
        on_delivery_lifetime_currency = Payment.objects.filter(payment_method="On Delivery").aggregate(Sum('cost'))
        on_delivery_today = Payment.objects.filter(date__date=today, payment_method="On Delivery").count()
        on_delivery_today_currency = Payment.objects.filter(date__date=today, payment_method="On Delivery").aggregate(Sum('cost'))

        context = {
            "payment_lifetime" : payment_lifetime,
            "payment_lifetime_currency" : payment_lifetime_currency,
            "payment_today" : payment_today,
            "payment_today_currency" : payment_today_currency,
            "statistics": statistics,
            "online_payment_lifetime": online_payment_lifetime,
            "online_payment_lifetime_currency": online_payment_lifetime_currency,
            "online_payment_today": online_payment_today,
            "online_payment_today_currency": online_payment_today_currency,
            "on_delivery_lifetime": on_delivery_lifetime,
            "on_delivery_lifetime_currency": on_delivery_lifetime_currency,
            "on_delivery_today": on_delivery_today,
            "on_delivery_today_currency": on_delivery_today_currency,
            "filter_cursor" : filter_cursor,
        }

        return render(request, 'payment.html', context)

    return redirect("/")


@login_required
def visitors(request):
    if request.user.is_staff:

        return render(request, 'visitors.html')

    return redirect("/")