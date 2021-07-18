from rest_framework import serializers
from mainsite.models import Product, author, publisher

class AllProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class OneProductsSerializer(serializers.ModelSerializer):
    publisher = serializers.StringRelatedField()
    author = serializers.StringRelatedField()
    #author_name = serializers.ReadOnlyField()
    class Meta:
        model = Product
        fields = ('id','title','release_year','pages','description','weight',
                  'price','discount_price','publisher','publisher_id','author',
                  'author_id','category','main_image','is_product_live',
                  'in_stock_number','ordered_times')

    def to_representation(self, data):
        result = super(OneProductsSerializer, self).to_representation(data)
        result['author'] = author.objects.get(id=attrs['author']).author_name
        result['publisher'] = publisher.objects.get(id=attrs['publisher']).publisher_name
        return result
