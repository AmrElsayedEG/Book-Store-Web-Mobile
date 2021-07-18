from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
from .recommendationsystem import recommendation
from .models import Product, Category, author, publisher
from orders.models import OrderItem, order
from django.contrib.auth.decorators import login_required
from cart.forms import CartAddProductForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.urls import reverse
from django.shortcuts import redirect
from accounts.models import users_wishlist
import json
from django.shortcuts import get_object_or_404
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import datetime
from bookstore import settings
from throttle.decorators import throttle


def home(request):
    #Advertising Banner
    ad = Product.objects.select_related('author').get(advertising_banner=1)
    #Top Sellers
    top_sellers = Product.objects.filter(is_product_live= 1).order_by('-ordered_times')[:3]
    #New Arrivals
    new_arrivals = Product.objects.filter(is_product_live= 1).order_by('-id')[:4]
    #####Wishlist
    my_wish_list = []
    if request.user.is_authenticated:
        my_wishlist = users_wishlist.objects.filter(user=request.user)
        my_wishlist = [my_wish_list.append(i.product_id) for i in my_wishlist]
    

    context = {
        'ad' : ad,
        'top_sellers' : top_sellers,
        'new_arrivals' : new_arrivals,
        'my_wishlist' : my_wish_list,
        }
    
    return render(request,'index.html', context)

##@login_required
##def download_ebooks(request):
##    if request.method == 'POST' and request.user:
##        book_id = request.POST['book_id']
##        user_orders = order.objects.filter(user=request.user)
##        buy = False
##        for i in user_orders:
##            try:
##                items = OrderItem.objects.get(order=i.id,product=book_id)
##                buy = True
##                book = Product.objects.get(id=book_id)
##                break
##            except:
##                buy = False
##        
##        if buy:
##            return HttpResponse("<script>window.onload = function(){var a = document.createElement('a');a.href = '%s';a.download = true;a.click();};</script>" % book.downloadable_file.url)
##        else:
##            return HttpResponse('Error Here')
##    else:
##        return HttpResponse('Error')

def all_books(request):
    all_cat = Category.objects.all()
    
    if 'cat' in request.GET:
        if request.GET.get('cat') == 'all':
            books = Product.objects.filter(is_product_live = 1).order_by('-id')
        else:
            cat_id = Category.objects.get(category_name = request.GET.get('cat'))
            books = Product.objects.filter(category = cat_id, is_product_live=1).order_by('-id')
    else:
        books = Product.objects.filter(is_product_live = 1).order_by('-id')
        
    paginator = Paginator(books, 15) #15
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if page_number is not None and page_number not in ['1', '2'] and page_obj.paginator.num_pages > 5:
        previous = int(page_number) - 2
        next = int(page_number) + 3
        if int(page_number) == page_obj.paginator.num_pages:
            previous = int(page_number) - 4
        elif int(page_number)+1 >= page_obj.paginator.num_pages:
            previous = int(page_number) - 3
        if next > page_obj.paginator.num_pages:
            next = page_obj.paginator.num_pages + 1
        pagin_range = range(previous, next)
    else:
        previous = 1
        next = 6
        if next > page_obj.paginator.num_pages:
            next = page_obj.paginator.num_pages + 1
        pagin_range = range(previous, next)
    #####Wishlist
    my_wish_list = []
    if request.user.is_authenticated:
        my_wishlist = users_wishlist.objects.filter(user=request.user)
        my_wishlist = [my_wish_list.append(i.product_id) for i in my_wishlist]
        
    context = {
        'all_cat' : all_cat,
        'page_obj':page_obj,
        'my_wishlist' : my_wish_list,
        'pagin_range' : pagin_range,
        }
    return render(request,'shop-page.html', context)

def search(request):
    #####Wishlist
    my_wish_list = []
    if request.user.is_authenticated:
        my_wishlist = users_wishlist.objects.filter(user=request.user)
        my_wishlist = [my_wish_list.append(i.product_id) for i in my_wishlist]
        
    if 'search' in request.GET:
        word = request.GET['search']
        books = Product.objects.filter(Q(author__author_name__icontains=word) | Q(title__icontains=word), is_product_live=1)
        paginator = Paginator(books, 15)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        if page_number is not None and page_number not in ['1', '2'] and page_obj.paginator.num_pages > 5:
            previous = int(page_number) - 2
            next = int(page_number) + 3
            if int(page_number) == page_obj.paginator.num_pages:
                previous = int(page_number) - 4
            elif int(page_number)+1 >= page_obj.paginator.num_pages:
                previous = int(page_number) - 3
            if next > page_obj.paginator.num_pages:
                next = page_obj.paginator.num_pages + 1
            pagin_range = range(previous, next)
        else:
            previous = 1
            next = 6
            if next > page_obj.paginator.num_pages:
                next = page_obj.paginator.num_pages + 1
            pagin_range = range(previous, next)
        context = {
            'page_obj':page_obj,
        'my_wishlist' : my_wish_list,
        'pagin_range' : pagin_range,
            }
        return render(request, 'search.html', context)
    else:
        return redirect(reverse('main:all_books'))

def one_book(request,slug):
    book = Product.objects.select_related('author').get(slug__iexact=slug)
    recommendations = recommendation(book.id)
    data = []
    for i in recommendations:
        data.append(int(i[1]))
    reco = Product.objects.filter(id__in = data)
    cart_product_form = CartAddProductForm()
    
    context = {
        'book' : book,
        'reco' : reco,
        'cart_product_form':cart_product_form,
        }
    return render(request,'product-page.html', context)

def get_author(request, id):
    author_query = get_object_or_404(author, id = id)
    books = Product.objects.filter(author = author_query).order_by('-id')
    paginator = Paginator(books, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if page_number is not None and page_number not in ['1', '2'] and page_obj.paginator.num_pages > 5:
        previous = int(page_number) - 2
        next = int(page_number) + 3
        if int(page_number) == page_obj.paginator.num_pages:
            previous = int(page_number) - 4
        elif int(page_number)+1 >= page_obj.paginator.num_pages:
            previous = int(page_number) - 3
        if next > page_obj.paginator.num_pages:
            next = page_obj.paginator.num_pages + 1
        pagin_range = range(previous, next)
    else:
        previous = 1
        next = 6
        if next > page_obj.paginator.num_pages:
            next = page_obj.paginator.num_pages + 1
        pagin_range = range(previous, next)

    #####Wishlist
    my_wish_list = []
    if request.user.is_authenticated:
        my_wishlist = users_wishlist.objects.filter(user=request.user)
        my_wishlist = [my_wish_list.append(i.product_id) for i in my_wishlist]

    context = {'author' : author_query,
               'page_obj' : page_obj,
               'my_wishlist' : my_wish_list,
                'pagin_range' : pagin_range,
               }
    return render(request,'author.html', context)

def get_publisher(request, id):
    publisher_query = get_object_or_404(publisher, id=id)
    books = Product.objects.filter(publisher = publisher_query).order_by('-id')
    paginator = Paginator(books, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if page_number is not None and page_number not in ['1', '2'] and page_obj.paginator.num_pages > 5:
        previous = int(page_number) - 2
        next = int(page_number) + 3
        if int(page_number) == page_obj.paginator.num_pages:
            previous = int(page_number) - 4
        elif int(page_number)+1 >= page_obj.paginator.num_pages:
            previous = int(page_number) - 3
        if next > page_obj.paginator.num_pages:
            next = page_obj.paginator.num_pages + 1
        pagin_range = range(previous, next)
    else:
        previous = 1
        next = 6
        if next > page_obj.paginator.num_pages:
            next = page_obj.paginator.num_pages + 1
        pagin_range = range(previous, next)
    #####Wishlist
    my_wish_list = []
    if request.user.is_authenticated:
        my_wishlist = users_wishlist.objects.filter(user=request.user)
        my_wishlist = [my_wish_list.append(i.product_id) for i in my_wishlist]

    context = {'publisher' : publisher_query,
               'page_obj' : page_obj,
               'my_wishlist' : my_wish_list,
              'pagin_range' : pagin_range,
               }
    return render(request,'publisher.html', context)

@throttle(zone='default')
def contact(request):
    status = 0
    if request.method == 'POST':
        subject = request.POST['subject']
        email_template_name = "contact-email-temp.html"
        c = {
            "fullname" : request.POST['fullname'],
            "email" : request.POST['email'],
            "message" : request.POST['message'],
            "date" : datetime.datetime.now().strftime("%Y-%m-%d")
            }
        email = render_to_string(email_template_name, c)
        try:
            msg = EmailMultiAlternatives(
                    subject, 'Book Store | Contact Request', to=[settings.EMAIL_HOST_USER]
                )
            msg.attach_alternative(email, "text/html")
            msg.send()
            status = 1
        except:
            status = 2
        
    context = {'status' : status}
    return render(request, 'contact.html', context)


def feedback_email(fullname, email, subject, message):
    email_template_name = "contact-email-temp.html"
    c = {
        "fullname": fullname,
        "email": email,
        "message": message,
        "date": datetime.datetime.now().strftime("%Y-%m-%d")
    }
    email = render_to_string(email_template_name, c)

    try:
        msg = EmailMultiAlternatives(
            subject, 'Book Store | Contact Request', to=[settings.EMAIL_HOST_USER]
        )
        msg.attach_alternative(email, "text/html")
        msg.send()
        return True
    except:
        return False
