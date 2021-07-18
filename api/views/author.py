from api.serializers import AllProductsSerializer, AllAuthorSerializer
from mainsite.models import Product, author
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

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