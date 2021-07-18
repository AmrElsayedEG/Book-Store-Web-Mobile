# import json
#
# from django.urls import reverse
# from django.contrib.auth.models import User
# from rest_framework import status
# from rest_framework.authtoken.models import Token
# from rest_framework.test import APITestCase
# from orders.models import order, OrderItem
# from mainsite.models import Product, coupon, author
# from accounts.models import Profile
#
# class RegisterTestCase(APITestCase):
#     def test_register(self):
#         data = {"password":"passwordd","password2":"passwordd",
#                 "email":"a@a.com","first_name":"Amr","last_name":"elsayed"}
#         response = self.client.post("/website-api/user-register/", data)
#         print(response.json())
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#
#
# class orderItemTestCase(APITestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username="amr",password="password")
#         self.token = Token.objects.create(user=self.user)
#         self.api_authentication()
#         self.orderModel = order.objects.create(user=self.user,customer_name='amr',
#                                                address_1='a',address_2='b',
#                                                postal_code='1',city='ca',
#                                                country='Egypt',phone='1',
#                                                payment_method='Paypal')
#         self.productModel = Product.objects.create(title='a',pages=1,
#                                     description='a',weight=1,price=1)
#         self.c = coupon.objects.create(code='aa',discount_percentage =50,active=1)
#
#
#     def api_authentication(self):
#         self.client.credentials(HTTP_AUTHORIZATION = "Token " + self.token.key)
#
#     def test_order_creation(self):
#         data = {'user':self.user,'customer_name':'amr',
#                                                'address_1':'a','address_2':'b',
#                                                'postal_code':'1','city':'ca',
#                                                'country':'Egypt','phone':'1',
#                                                'payment_method':'PayPal',
#                 'token':self.token.key,'coupon':self.c.id}
#         response = self.client.post("/website-api/create-order/", data=data)
#         print(response.json())
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#
#     def test_order_item_creation(self):
#         data = {'order':self.orderModel.id,'product':self.productModel.id,'price':'30'
#                 ,'quantity':'30'}
#         response = self.client.post("/website-api/create-order-item/", data=data)
#         print(response.json())
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         #self.assertEqual(response.data['id'], self.orderModel.id)
#
#     def test_lsit_order_item_creation(self):
#         data = {1:[self.orderModel.id,self.productModel.id,'30'
#                 ,'30'],
#                2:[self.orderModel.id,self.productModel.id,'30'
#                 ,'30']}
#         response = self.client.post("/website-api/create-order-item/", data=data)
#         print(response.json())
#         print("Order",self.orderModel.id)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         response = self.client.get("/website-api/my-orders/?token={}".format(self.token.key))
#         print(response.json())
#         response = self.client.get("/website-api/items-per-order/{}/".format(self.orderModel.id))
#         print(response.json())
#
#     def test_order_item_creation_non_user(self):
#         self.client.force_authenticate(user=None)
#         data = {'order':self.orderModel,'product':self.productModel,'price':'30'
#                 ,'quantity':'30'}
#         response = self.client.post("/website-api/create-order-item/", data)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#
# class AccountTestCase(APITestCase):
#     def setUp(self):
#         self.c = coupon.objects.create(code='aa',discount_percentage =50,active=1)
#         self.user = User.objects.create_user(username="amr",password="password")
#         self.token = Token.objects.create(user=self.user)
#         self.api_authentication()
#         self.orderModel = order.objects.create(user=self.user,customer_name='amr',
#                                                address_1='a',address_2='b',
#                                                postal_code='1',city='ca',
#                                                country='Egypt',phone='1',
#                                                payment_method='Paypal',coupon=self.c)
#         self.productModel = Product.objects.create(title='a',pages=1,
#                                     description='a',weight=1,price=1)
#         self.item = OrderItem.objects.create(order=self.orderModel,product=self.productModel,
#                                              price=10,quantity=1)
#
#
#     def api_authentication(self):
#         self.client.credentials(HTTP_AUTHORIZATION = "Token " + self.token.key)
#
#     def test_my_orders(self):
#         response = self.client.get("/website-api/my-orders/?token={}".format(self.token.key))
#         print(response.json())
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_get_my_prifle_info(self):
#         response = self.client.get("/website-api/profile/{}/?token={}".format(self.user.id,self.token.key))
#         print(response.json())
#
#     def test_post_my_prifle_info(self):
#         data = {
#                 'country': 'Egypt', 'city': 'Cairo', 'postal_code': 'postal',
#                 'address_1': 'Address 1',
#                 'address_2': 'Address 2', 'phone': '01xxxxxxxx','user':self.user.id
#                 }
#         response = self.client.put("/website-api/profile/{}/?token={}".format(self.user.id,self.token.key), data)
#         print(response.json())
#         print(">>>>>",Profile.objects.get(user=self.user).city)
#
#     def test_get_my_user_info(self):
#         response = self.client.get("/website-api/user/{}/?token={}".format(self.user.id,self.token.key))
#         print(response.json())
#
#     def test_post_my_user_info(self):
#         data = {
#                'first_name':'amr',
#                'last_name':'elsayed',
#                'user':self.user.id
#                 }
#         response = self.client.put("/website-api/user/{}/?token={}".format(self.user.id,self.token.key), data)
#         print(response.json())
#         print(">>>>>",User.objects.get(id=self.user.id).first_name)
#
#     def test_change_password(self):
#         data = {
#             'token':self.token.key,
#             'old_password':'password',
#             'password1':'test'
#             }
#         response = self.client.post("/website-api/password/change/", data)
#         print(response.json())
#
#
#
# class RecommendationTestCase(APITestCase):
#
#     def setUp(self):
#         self.a = author.objects.create(author_name='amr')
#         Product.objects.create(title='a', pages=1, description='a', weight=1, price=1, author=self.a)
#         Product.objects.create(title='b', pages=1, description='a', weight=1, price=1)
#         Product.objects.create(title='c', pages=1, description='a', weight=1, price=1, author=self.a)
#         Product.objects.create(title='d', pages=1, description='a', weight=1, price=1)
#
#     def test_reco(self):
#         response = self.client.get("/website-api/product-reco/1/")
#         print(response.json())
#
#     def test_get_author(self):
#         response = self.client.get("/website-api/authors/{}/".format(self.a.id))
#         print(response.json())
