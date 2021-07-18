from api.serializers import AllProductsSerializer, AllPublisherSerializer
from mainsite.models import Product, publisher
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

class OnePublisherAPI(generics.ListAPIView):
    queryset = publisher.objects.all()
    serializer_class = AllPublisherSerializer
    lookup_field = 'id'
    def get_queryset(self):
      queryset = publisher.objects.filter(pk=self.kwargs['id'])
      return queryset

class One_PublisherProductsAPI(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = AllProductsSerializer
    pagination_class = PageNumberPagination
    def get_queryset(self):
        queryset = Product.objects.filter(publisher=self.request.query_params.get('publisher')).order_by('-id')
        return queryset