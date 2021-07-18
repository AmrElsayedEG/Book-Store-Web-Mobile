from .serializers import OneProductsSerializer
from mainsite.models import Product
from rest_framework import generics

class OneProductAPI(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = OneProductsSerializer
    lookup_field = 'id'
    def get_queryset(self):
      queryset = Product.objects.filter(pk=self.kwargs['id'])
      return queryset