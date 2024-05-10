from rest_framework import serializers
from payapp.models import ConversionResponse

class ConversionResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversionResponse
        fields = ('__all__')


