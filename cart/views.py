from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from mainsite.models import Product, coupon
from orders.models import order
from .cart import Cart
from .forms import CartAddProductForm
from django.http import HttpResponse


# Create your views here.

@require_POST
def cart_add(request, product_id):
	if request.session.get('total_cost') is not None:
		del request.session['total_cost']
	cart = Cart(request)
	product = get_object_or_404(Product, id=product_id)
	form = CartAddProductForm(request.POST)
	if form.is_valid():
		cd = form.cleaned_data
		cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
	return redirect('cart:cart_detail')


def cart_remove(request, product_id):
	if request.session.get('total_cost') is not None:
		del request.session['total_cost']
	cart = Cart(request)
	product = get_object_or_404(Product, id=product_id)
	cart.remove(product)
	return redirect('cart:cart_detail')


def cart_detail(request):
	r = request.user
	cart = Cart(request)
	price_after_discount = None

	for item in cart:
		item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})



	context = {
		'cart': cart,
		'r': r,
		'price_after_discount': price_after_discount
	}

	return render(request, 'cart-page.html', context)
