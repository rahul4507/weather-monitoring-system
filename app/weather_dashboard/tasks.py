import requests
from django.db import models

from .models import City, WeatherUpdate, DailySummary
from celery import shared_task
from django.utils import timezone
from django.db.models import Avg, Max, Min

API_KEY = '79f656627db44aa18758a5d09b87b33d'

@shared_task
def fetch_weather_data():
    cities = City.objects.all()
    for city in cities:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city.name}&appid={API_KEY}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            temp = data['main']['temp'] - 273.15  # Convert from Kelvin to Celsius
            feels_like = data['main']['feels_like'] - 273.15
            weather_condition = data['weather'][0]['main']
            timestamp = timezone.now()

            WeatherUpdate.objects.create(
                city=city,
                temp=temp,
                feels_like=feels_like,
                weather_condition=weather_condition,
                timestamp=timestamp
            )


@shared_task
def calculate_daily_summary():
    cities = City.objects.all()
    today = timezone.now().date()

    for city in cities:
        updates = WeatherUpdate.objects.filter(city=city, timestamp__date=today)

        if updates.exists():
            avg_temp = updates.aggregate(Avg('temp'))['temp__avg']
            max_temp = updates.aggregate(Max('temp'))['temp__max']
            min_temp = updates.aggregate(Min('temp'))['temp__min']
            dominant_weather = updates.values('weather_condition').annotate(count=models.Count('weather_condition')).order_by('-count').first()['weather_condition']

            DailySummary.objects.create(
                city=city,
                date=today,
                avg_temp=avg_temp,
                max_temp=max_temp,
                min_temp=min_temp,
                dominant_weather=dominant_weather
            )

@shared_task
def check_alerts():
    cities = City.objects.all()
    threshold_temp = 35.0  # Configurable

    for city in cities:
        recent_updates = WeatherUpdate.objects.filter(city=city).order_by('-timestamp')[:2]
        if len(recent_updates) == 2:
            if all(update.temp > threshold_temp for update in recent_updates):
                print(f"Alert: Temperature exceeded {threshold_temp}°C in {city.name} for two consecutive updates.")
                # Optionally send an email or other notifications