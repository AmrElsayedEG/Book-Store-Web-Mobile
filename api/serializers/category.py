from rest_framework import serializers
from mainsite.models import Category

class AllCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'