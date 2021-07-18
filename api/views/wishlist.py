from api.serializers import WishlistSerializer
from rest_framework.permissions import IsAuthenticated
from accounts.models import users_wishlist
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

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