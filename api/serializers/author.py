from rest_framework import serializers
from mainsite.models import author

class AllAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = author
        fields = '__all__'