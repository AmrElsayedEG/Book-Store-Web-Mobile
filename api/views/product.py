from api.serializers import AllProductsSerializer, OneProductsSerializer
from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from mainsite.models import Product

class All_ProductsAPI(generics.ListAPIView):
    queryset = Product.objects.filter(is_product_live = 1).order_by('-id')
    serializer_class = AllProductsSerializer
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title', 'author__author_name', 'publisher__publisher_name')

class OneProductAPI(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = OneProductsSerializer
    lookup_field = 'id'
    def get_queryset(self):
      queryset = Product.objects.filter(pk=self.kwargs['id'])
      return queryset