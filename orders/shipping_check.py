from django.http import HttpResponse
import json
from mainsite.models import shipping_fee
from cart.cart import Cart


def get_shipping_fees(request):
    ##### AJAX
    if request.method == 'POST' and request.is_ajax():
        cart = Cart(request)
        s_s = request.session.get('total_cost')
        if s_s is None:
            s_s = cart.get_total_cost()
        city = request.POST['city']
        fees_model = shipping_fee.objects.filter(city__iexact=city)
        if fees_model.exists():
            fees_model = fees_model.last()
            new_price = float(s_s) + float(fees_model.fees)
            request.session['city_fees'] = float(fees_model.fees)
            res = {'status' : 'Success', 'fees' : fees_model.fees, 'new_price' : new_price}
            return HttpResponse(json.dumps(res), content_type='application/json')
                    
        else:
            fees_model = shipping_fee.objects.get(city='default')
            new_price = float(s_s) + float(fees_model.fees)
            request.session['city_fees'] = float(fees_model.fees)
            res = {'status' : 'Success', 'fees' : fees_model.fees, 'new_price': new_price}
            return HttpResponse(json.dumps(res), content_type='application/json')
    #########
