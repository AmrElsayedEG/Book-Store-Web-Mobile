from django.contrib.auth.models import User
from .serializers import (UserSerializer, ProfileSerializer, RegisterSerializer, AllProductsSerializer,
                            OrderSerializer, OrderItemSerializer, AllAuthorSerializer,
                            AllPublisherSerializer, AllCategorySerializer, OneProductsSerializer, WishlistSerializer, MyOrderNewSerializer)
from mainsite.models import Product, author, publisher, Category, coupon, shipping_fee
from mainsite.views import feedback_email
from orders.models import order, OrderItem
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from accounts.models import Profile, users_wishlist
from django.shortcuts import render, redirect
from django.http import JsonResponse
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .hash import encode
from orders.views import order_info_email
from bookstore.settings import SITE_URL
from django.core.mail import EmailMultiAlternatives
from rest_framework.views import APIView

class RegisterAPI(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        reg_user = self.serializer_class(data=self.request.data)
        reg_user.is_valid(raise_exception=True)
        reg_user.save()
        return Response({"success": "Check your Email to activate your account."})
        

class All_ProductsAPI(generics.ListAPIView):
    queryset = Product.objects.filter(is_product_live = 1).order_by('-id')
    serializer_class = AllProductsSerializer
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title', 'author__author_name', 'publisher__publisher_name')

class OffersAPI(APIView, PageNumberPagination):
    #pagination_class = PageNumberPagination
    def get(self, request):
        all = Product.objects.all().exclude(discount_price=None)
        all_dict = {}
        for i in all:
            all_dict[i.id] = ((i.price - i.discount_price) * 100) / i.price
        all_dict = sorted(all_dict, key=all_dict.get, reverse=True)
        all = dict([(obj.id, obj) for obj in all])
        sorted_objects = [all[id] for id in all_dict]
        results = self.paginate_queryset(sorted_objects, request, view=self)
        serializer = AllProductsSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)

class All_CategoriesAPI(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = AllCategorySerializer

class One_CategoryProductsAPI(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = AllProductsSerializer
    pagination_class = PageNumberPagination
    def get_queryset(self):
        queryset = Product.objects.filter(category=self.request.query_params.get('cat'), is_product_live = 1).order_by('-id')
        return queryset
        

class OneProductAPI(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = OneProductsSerializer
    lookup_field = 'id'
    def get_queryset(self):
      queryset = Product.objects.filter(pk=self.kwargs['id'])
      return queryset

class orderAPI(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = order.objects.all()
    serializer_class = OrderSerializer
    def perform_create(self, serializer):
        user_token = Token.objects.get(key = self.request.data['token'])
        userid = user_token.user_id
        u = User.objects.get(id=userid)
        serializer.save(user=u)

class orderItemAPI(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

    def post(self, request,*args, **kwargs):
        a = dict(self.request.data)
        if isinstance(a, dict):
            obj = []
            for k,v in a.items():
                d = {'order' : v[0], 'product' : v[1],'price' : v[2],
                     'quantity' : v[3]}
                orderItem = OrderItemSerializer(data = d)
                orderItem.is_valid(raise_exception=True)
                obj.append(orderItem)
            for ob in obj:
                ob.save()
        return Response({"success": "Order Submitted."})

class CouponAPI(APIView):
    
    def get(self, request, *args, **kwargs):
        return Response({'error':'Wrong Coupon Code'})
    
    def post(self, request, *args, **kwargs):
        try:
            queryset = coupon.objects.filter(code=self.request.data['code'])
            if queryset[0].active == False:
                return Response({'error':'Coupon Code Expired'})
            prev = order.objects.filter(coupon=queryset[0],user_id=self.request.data['user_id'])
            if prev.exists():
                return Response({'error':'You already used this coupon'})
            return Response({'id':queryset[0].id,'discount_percentage':queryset[0].discount_percentage})
        except:
            return Response({'error':'Wrong Coupon Code'})

##AUTHORS
class OneAuthorAPI(generics.ListAPIView):
    queryset = author.objects.all()
    serializer_class = AllAuthorSerializer
    lookup_field = 'id'
    def get_queryset(self):
      queryset = author.objects.filter(pk=self.kwargs['id'])
      return queryset

class One_AuthorProductsAPI(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = AllProductsSerializer
    pagination_class = PageNumberPagination
    def get_queryset(self):
        queryset = Product.objects.filter(author=self.request.query_params.get('author')).order_by('-id')
        return queryset


#PUBLISHERS
class OnePublisherAPI(generics.ListAPIView):
    queryset = publisher.objects.all()
    serializer_class = AllPublisherSerializer
    lookup_field = 'id'
    def get_queryset(self):
      queryset = publisher.objects.filter(pk=self.kwargs['id'])
      return queryset

class One_PublisherProductsAPI(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = AllProductsSerializer
    pagination_class = PageNumberPagination
    def get_queryset(self):
        queryset = Product.objects.filter(publisher=self.request.query_params.get('publisher')).order_by('-id')
        return queryset

class MyOrdersAPI(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = order.objects.all()
    serializer_class = MyOrderNewSerializer
    def get_queryset(self):
      user_token = Token.objects.get(key = self.request.query_params.get('token'))
      userid = user_token.user_id
      queryset = order.objects.filter(user=userid).order_by('-id')
      return queryset


class ProfileAPI(generics.RetrieveUpdateAPIView):
    """
    A viewset for viewing and editing user instances.
    """
    permission_classes = (IsAuthenticated,)
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'user_id'
    def get_queryset(self):
      user_token = Token.objects.get(key = self.request.query_params.get('token'))
      userid = user_token.user_id
      queryset = Profile.objects.filter(user_id=userid)
      return queryset


class UserAPI(generics.RetrieveUpdateAPIView):
    """
    A viewset for viewing and editing user instances.
    """
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'
    def get_queryset(self):
      user_token = Token.objects.get(key = self.request.query_params.get('token'))
      userid = user_token.user_id
      queryset = User.objects.filter(id=userid)
      return queryset

from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.core.mail import BadHeaderError
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def forget_password(request):
    if request.method == 'POST':
        data = request.POST['email']
        associated_users = User.objects.filter(Q(email=data))
        if associated_users.exists():
            for user in associated_users:
                subject = "Password Reset Requested"
                email_template_name = "password/password_reset_subject.html"
                c = {
					    "email":user.email,
					    'domain':SITE_URL,
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
                    return JsonResponse({"success" : "An email has been sent to you"}, safe=False)
                except BadHeaderError:
                    return JsonResponse({"error" : "Error, Please Try Again!"}, status=400, safe=False)
        else:
            return JsonResponse({"error" : "An account with this email not found."}, status=400, safe=False)
    return JsonResponse("404 Not Found", safe=False)




@csrf_exempt
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('password1')
        token = request.POST.get('token')
        user_token = Token.objects.get(key = token)
        userid = user_token.user_id
        u = User.objects.get(id=userid)
        check = check_password(u,old_password)
        if check:
            u.set_password(new_password)
            u.save()
            return JsonResponse({'success':'Password Changed'}, safe=False)
        else:
            return JsonResponse({'error':'Your old password is wrong'}, status=400, safe=False)
    else:
        return JsonResponse("404 Not Found", safe=False)

def check_password(user_model,old_password):
    return user_model.check_password(old_password)

        
class encodeAPI(APIView):

    def post(self, request):
        if 'sec_key' in self.request.data:
            return Response({"sec_key" : encode(request.data['sec_key'])})
        return Response({'error':'Bad params'}, status=400)

class OrderEmailAPI(APIView):

    def post(self, request):
        if 'orderid' in self.request.data:
            order_info_email(request.data['orderid'])
            return Response({"success" : "Order info sent to your Email."})
        return Response({'error':'Bad params'}, status=400)




class wishListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if 'token' in self.request.query_params:
            user_token = Token.objects.get(key = self.request.query_params['token']).user_id
            return Response({"results" : WishlistSerializer(users_wishlist.objects.filter(user=user_token).order_by('-id'), many=True).data})
        return Response({'error':'Bad params'}, status=400)

    def post(self, request):
        if {"token", "id"} <= self.request.data.keys():
            user_token = Token.objects.get(key = self.request.data['token']).user
            wish_list = users_wishlist.objects.filter(user=user_token, product=self.request.data['id'])
            if not wish_list.exists():
                users_wishlist.objects.create(user=user_token, product_id=self.request.data['id'])
                return Response({'success' : 'Product Added to your wishlist'})
            wish_list = wish_list.last().delete()
            return Response({'success' : 'Product Deleted from your wishlist'})
        return Response({'error' : 'Wrong Params'}, status=400)

class shippingFeesView(APIView):
    def get(self, request):
        if 'city' in self.request.query_params:
            fees_model = shipping_fee.objects.filter(city__iexact=self.request.query_params['city'])
            if fees_model.exists():
                fees_model = fees_model.last()
                return Response({'success' : fees_model.fees})
            fees_model = shipping_fee.objects.get(city='default')
            return Response({'success' : fees_model.fees})
        return Response({'error' : 'wrong params'}, status=400)

class feedback(APIView):

    def post(self, request):
        fb_email = feedback_email(fullname=self.request.data['fullname'],
                               email=self.request.data['email'],
                               subject=self.request.data['subject'],
                               message=self.request.data['message'])
        if fb_email is True:
            return Response({'success' : 'We recieved your feedback and will get back to you soon.'})
        return Response({'error' : 'Something went wrong, Please try again'}, status=400)
