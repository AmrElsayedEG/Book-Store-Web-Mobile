from api.serializers import AllProductsSerializer
from mainsite.models import Product
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView


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
