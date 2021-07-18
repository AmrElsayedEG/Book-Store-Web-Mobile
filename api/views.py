from rest_framework.response import Response
from mainsite.recommendationsystem import recommendation
from django.http import JsonResponse
from mainsite.models import Product
from .serializers import AllProductsSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                       context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
                'token': token.key,
                'user_id': user.pk
        })


def aiapi(reuqest,id):
    res = recommendation(id)
    data = []
    prod = []
    for i in res:
        data.append(int(i[1]))
        prod.append(Product.objects.get(id=int(i[1])))
    prod_ser = AllProductsSerializer(prod, many=True).data
    return JsonResponse(prod_ser, safe=False)