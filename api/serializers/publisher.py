
from rest_framework import serializers
from mainsite.models import publisher

class AllPublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = publisher
        fields = '__all__'