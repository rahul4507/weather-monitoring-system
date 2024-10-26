from rest_framework import serializers
from .models import DailySummary


class DailySummarySerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(source='city.name')
    date = serializers.SerializerMethodField()

    class Meta:
        model = DailySummary
        fields = ['city_name', 'date', 'avg_temp', 'min_temp', 'max_temp', 'dominant_weather']

    def get_date(self, obj):
        # Format the date as "Month day, Year" (e.g., "October 26, 2024")
        return obj.date.strftime("%B %d, %Y %H:%M:%S")
