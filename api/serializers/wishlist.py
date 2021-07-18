from rest_framework import serializers
from accounts.models import users_wishlist
from .products import AllProductsSerializer

class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = users_wishlist
        fields = ('id', 'product',)

    def to_representation(self, data):
        query = AllProductsSerializer(data.product).data
        return query
