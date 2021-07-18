from .serializers.products import AllProductsSerializer
from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination

class All_ProductsAPI(generics.ListAPIView):
    queryset = Product.objects.filter(is_product_live = 1).order_by('-id')
    serializer_class = AllProductsSerializer
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title', 'author__author_name', 'publisher__publisher_name')