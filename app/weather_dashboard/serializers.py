from rest_framework import serializers
from .models import DailySummary, City

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name']

class DailySummarySerializer(serializers.ModelSerializer):
    city = CitySerializer()  # Nested serializer to include city details

    class Meta:
        model = DailySummary
        fields = ['city', 'date', 'avg_temp', 'max_temp', 'min_temp', 'dominant_weather']
