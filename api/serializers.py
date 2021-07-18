from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from mainsite.models import Product, author, publisher, Category, coupon
from orders.models import order, OrderItem
from accounts.models import Profile, users_wishlist

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }
        read_only_fields =  ('username',)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"error": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['email'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_active = False
        )

        
        user.set_password(validated_data['password'])
        user.save()

        return user
 

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

    def get(self,attrs):
        attrs['author'] = author.objects.get(id=attrs['author']).author_name
        attrs['publisher'] = publisher.objects.get(id=attrs['publisher']).publisher_name
        return attrs


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
    #product = serializers.CharField()
    product_title = serializers.ReadOnlyField(source='product.title')
    product_image = serializers.CharField(source='product.main_image.url')
    total = TotalCostField(source='*')
    
    class Meta:
        model = OrderItem
        fields = ('order_id','product_id','price','quantity','product_title'
                  ,'product_image', 'total')


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = coupon
        fields = '__all__'

class AllAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = author
        fields = '__all__'

class AllPublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = publisher
        fields = '__all__'

class AllCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

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


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('first_name','last_name', 'email',)
        

class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = users_wishlist
        fields = ('id', 'product',)

    def to_representation(self, data):
        #query = super(WishlistSerializer,self).to_representation(data)
        query = AllProductsSerializer(data.product).data
        return query
