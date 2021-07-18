from rest_framework import serializers
from orders.models import order, OrderItem


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = order
        fields = '__all__'
        read_only_fields =  ('user',)


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class TotalCostField(serializers.Field):

    def to_representation(self, value):
        ret = value.price * value.quantity
        return ret

    def to_internal_value(self, data):
        ret = value.price * value.quantity
        return ret

class ItemsPerOrderSerializer(serializers.ModelSerializer):
    product_title = serializers.ReadOnlyField(source='product.title')
    product_image = serializers.CharField(source='product.main_image.url')
    total = TotalCostField(source='*')
    
    class Meta:
        model = OrderItem
        fields = ('order_id','product_id','price','quantity','product_title'
                  ,'product_image', 'total')

class TotalCostPerOrderField(serializers.Field):

    def to_representation(self, value):
        ret = order.objects.get(id=value.id).get_total_cost()
        return ret

    def to_internal_value(self, data):
        ret = order.objects.get(id=value.id)
        return ret

class MyOrdersSerializer(serializers.ModelSerializer):
    total_cost = TotalCostPerOrderField(source='*')
    class Meta:
        model = order
        exclude = ('usd_amount',)
        extra_fields = ['total_cost']

class MyOrderNewSerializer(serializers.ModelSerializer):
    total_cost = TotalCostPerOrderField(source='*')
    class Meta:
        model = order
        exclude = ('usd_amount', )
        extra_fields = ['total_cost']

    def to_representation(self, data):
        query = super(MyOrderNewSerializer,self).to_representation(data)
        query['items'] = ItemsPerOrderSerializer(OrderItem.objects.filter(order = data.id), many=True).data
        return query

