from rest_framework import serializers
from products.models import Box

class BoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = [
            'length',
            'width',
            'height',
            'volume',
            'area',
            'created_by',
            'last_updated_date',
        ]
