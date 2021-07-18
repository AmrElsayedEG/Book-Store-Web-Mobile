from api.serializers import MyOrderNewSerializer
from orders.models import order
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

class MyOrdersAPI(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = order.objects.all()
    serializer_class = MyOrderNewSerializer
    def get_queryset(self):
      user_token = Token.objects.get(key = self.request.query_params.get('token'))
      userid = user_token.user_id
      queryset = order.objects.filter(user=userid).order_by('-id')
      return queryset