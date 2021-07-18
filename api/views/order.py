from django.contrib.auth.models import User
from api.serializers import OrderSerializer, OrderItemSerializer
from orders.models import order, OrderItem
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

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