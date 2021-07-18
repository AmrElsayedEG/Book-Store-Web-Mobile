from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from accounts.models import Profile
from orders.models import order, OrderItem
from .forms import profileForm,userForm
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.core.mail import BadHeaderError
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse
from .models import users_wishlist
import json

# Create your views here.
UserModel = get_user_model()
from .tokens import account_activation_token
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Profile
def signpage(request):
    if request.user.is_authenticated:
        return redirect(reverse('accounts:dashboard'))
    if request.method == 'POST':
        signupmsg = False
        error = False
        exist = False
        if 'signin-btn' in request.POST:
            username = request.POST['email']
            password = request.POST['password']
            user = authenticate(request,username=username, password=password)
            if user is not None:
                login(request, user)
                if Profile.objects.get(user=request.user).address_1 == 'Address 1':
                    return redirect(reverse('accounts:edit-personal'))
                return redirect(reverse('accounts:dashboard'))
            #redirect to profile
            else:
                #invalid login
                error = True
        if 'signup-btn' in request.POST:
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            email = request.POST['email']
            password1 = request.POST['password1']
            try:
                user = User.objects.create_user(username = email, password=password1, email= email, first_name=firstname,last_name=lastname)
                user.is_active = False
                user.save()
                signupmsg = True
            except:
                exist = True
            # return to check mail
    else:
        #Return Forms
        signupmsg = False
        error = False
        exist = False
    context = {
        'signupmsg' : signupmsg,
        'activate' : activate,
        'error' : error,
        'exist' : exist,
        }
    return render(request, 'sign-in-page.html', context)

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # Return Email Activated redirect to login
    else:
        #return HttpResponse('Activation link is invalid!')
        return redirect("/")
    return render(request, 'acc-activated.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse('main:main_site_home'))

##def profile_info(request):
##    profile = get_object_or_404(Profile,user=request.user)
##    context = {
##        'profile':profile,
##    }
##    return HttpResponse(profile)
##    #return render(request,'user-profile.html',context)

@login_required
def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    status = 0
    if request.method == 'POST':
        user_form = userForm(request.POST, request.FILES, instance=request.user)
        profile_form = profileForm(request.POST, instance=profile)
        print(user_form)
        print(profile_form)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            status = 1
        else:
            status = 2
    else:
        user_form = userForm(instance=request.user)
        profile_form = profileForm(instance=profile)
    context = {
        'user_form':user_form,
        'profile_form':profile_form,
        'status' : status,
    }
    return render(request,'profile-page.html',context)

@login_required
def dashboard(request):
    orders = order.objects.filter(user=request.user)
    context = {
        'orders' : orders,
        }
    return render(request,'dashboard-page.html',context)

@login_required
def one_order(request,id):
    orders = get_object_or_404(order, id=id)
    items = OrderItem.objects.filter(order=orders.id).select_related('product')
    if orders.user == request.user:
        context = {'orders':orders,'items':items}
    else:
        # 404 Page
        return render(request, '404.html')
    return render(request,'order-details-page.html',context)
##################
# Forget Password


def password_reset_request(request):
    invalid_mail = False
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            host = request.get_host()
            if associated_users.exists():
                    for user in associated_users:
                        subject = "Password Reset Requested"
                        email_template_name = "password/password_reset_subject.html"
                        c = {
					    "email":user.email,
					    'domain':settings.SITE_URL,
					    'site_name': 'TriTlas | Egypt',
					    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
					    "user": user,
					    'token': default_token_generator.make_token(user),
					    }
                        email = render_to_string(email_template_name, c)
                    try:
                        msg = EmailMultiAlternatives(subject, 'Book Store', to=[user.email])
                        msg.attach_alternative(email, "text/html")
                        msg.send()
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect ("/account/reset/password_reset/done/")
            invalid_mail = True
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form,"invalid_mail":invalid_mail})
###################


# Change Password
@login_required
def change_password(request):
    status = 0
    if request.method == 'POST':
        old_password = request.POST['old_password']
        new_password = request.POST['password1']
        u = User.objects.get(id=request.user.id)
        check = check_password(u,old_password)
        if check:
            u.set_password(new_password)
            u.save()
            status = 1
        else:
            status=2
    context = { 'status' : status }
    return render(request, 'change-pwd.html', context)

def check_password(user_model,old_password):
    return user_model.check_password(old_password)


@login_required
def my_wish(request):
    my_w = users_wishlist.objects.filter(user = request.user).select_related('product')
    if request.method == 'POST':
        print(request.POST)
        item = request.POST['wish-item-id']
        users_wishlist.objects.get(id=item).delete()
    context = {'my_w' : my_w, }
    return render(request, 'wishlist.html', context)




def wish_req(request):
    #####Wishlist
    if request.method == 'POST' and request.is_ajax():
        wishID = request.POST.get('wishlist-id')
        a = users_wishlist.objects.filter(user=request.user, product_id = int(wishID))
        if a.exists():
            a = a.first()
            a.delete()
            res = {'status' : 'deleted'}
            return HttpResponse(json.dumps(res), content_type='application/json')
        
        users_wishlist.objects.create(user=request.user, product_id= int(wishID))
        res = {'status' : 'success'}
        return HttpResponse(json.dumps(res), content_type='application/json')
    #########
