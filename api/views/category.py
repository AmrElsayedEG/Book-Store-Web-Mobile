from django.contrib.auth.models import User
from .serializers import AllProductsSerializer, AllCategorySerializer
from mainsite.models import Product, Category
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

class All_CategoriesAPI(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = AllCategorySerializer

class One_CategoryProductsAPI(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = AllProductsSerializer
    pagination_class = PageNumberPagination
    
    def get_queryset(self):
        queryset = Product.objects.filter(category=self.request.query_params.get('cat'), is_product_live = 1).order_by('-id')
        return queryset
        