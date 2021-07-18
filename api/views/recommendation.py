from mainsite.recommendationsystem import recommendation
from django.http import JsonResponse
from mainsite.models import Product
from api.serializers import AllProductsSerializer
from rest_framework.response import Response

def aiapi(reuqest,id):
    res = recommendation(id)
    data = []
    prod = []
    for i in res:
        data.append(int(i[1]))
        prod.append(Product.objects.get(id=int(i[1])))
    prod_ser = AllProductsSerializer(prod, many=True).data
    return JsonResponse(prod_ser, safe=False)