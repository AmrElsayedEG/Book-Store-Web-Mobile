from rest_framework import serializers
from mainsite.models import coupon

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = coupon
        fields = '__all__'
