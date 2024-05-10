from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ConversionResponseSerializer
# Create your views here.

CONVERSION_RATES = {
    'EUR': {'EUR': 1.0, 'GBP': 0.86, 'USD': 1.07},
    'GBP': {'EUR': 1.16, 'GBP': 1.0, 'USD': 1.25},
    'USD': {'EUR': 0.93, 'GBP': 0.8, 'USD': 1.0},
}


class Conversion(generics.CreateAPIView):
    serializer_class = ConversionResponseSerializer

    def get(self, request, original_currency, destination_currency, amount):

        if original_currency not in CONVERSION_RATES or destination_currency not in CONVERSION_RATES:
            return Response({'error': 'Invalid currency'}, status=status.HTTP_400_BAD_REQUEST)

        conversion_rate = CONVERSION_RATES[original_currency][destination_currency]
        destination_amount = float(amount) * float(conversion_rate)

        queryset = ConversionResponseSerializer({'conversion_rate': conversion_rate, 'destination_amount': destination_amount})

        return Response(queryset.data, status=status.HTTP_200_OK)






