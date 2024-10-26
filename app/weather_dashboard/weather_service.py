from datetime import datetime

import requests
from django.conf import settings
from django.db.models import Avg, Max, Min, Count
from .models import City, WeatherUpdate, DailySummary, UserPreference
from .utils import convert_temperature

API_URL = settings.API_URL
API_KEY = settings.API_KEY
CITIES = settings.CITIES


def fetch_weather_data():
    for city_name in CITIES:
        params = {
            'q': city_name,
            'appid': API_KEY
        }
        response = requests.get(API_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            process_weather_data(city_name, data)
        else:
            print(f"Error fetching data for {city_name}: {response.status_code}")


def process_weather_data(city_name, data):
    user_preference = UserPreference.objects.first()
    temp_pref = user_preference.temperature_preference if user_preference else UserPreference.TemperaturePreference.CELSIUS

    # Parse weather data
    main = data.get('main', {})
    weather = data.get('weather', [{}])[0]
    weather_condition = weather.get('main', 'Unknown')
    temp = convert_temperature(main.get('temp'), temp_pref)
    min_temp = convert_temperature(main.get('temp_min'), temp_pref)
    max_temp = convert_temperature(main.get('temp_max'), temp_pref)
    feels_like = convert_temperature(main.get('feels_like'), temp_pref)
    dt = data['dt']  # Unix timestamp
    # Save to WeatherUpdate model
    city, created = City.objects.get_or_create(name=city_name)
    weather_obj = WeatherUpdate.objects.create(
        weather_condition=weather_condition,
        temp=temp, min_temp=min_temp, max_temp=max_temp, feels_like=feels_like,
        dt=dt, city=city,
    )
    date_with_timestamp = datetime.fromtimestamp(weather_obj.dt)
    # Aggregate daily summary update
    aggregate_daily_summary(city, date_with_timestamp, temp, min_temp, max_temp, weather_condition)


def aggregate_daily_summary(city, date_with_timestamp, temp, min_temp, max_temp, weather_condition):
    daily_summary = DailySummary.objects.filter(
        city=city,
        date__date=date_with_timestamp.date()  # Query for today's entry (date only)
    ).first()
    if daily_summary is None:
        # If no entry exists for today, create a new one
        daily_summary = DailySummary.objects.create(
            city=city,
            date=date_with_timestamp,  # Store the full datetime (with time)
            avg_temp=temp,
            min_temp=min_temp,
            max_temp=max_temp,
            dominant_weather=weather_condition
        )
    else:
        aggregated_data = WeatherUpdate.objects.filter(city=city, created_at__date=date_with_timestamp.date()).aggregate(
            min_temp=Min('temp'),
            max_temp=Max('temp'),
            avg_temp=Avg('temp')
        )
        daily_summary.date = date_with_timestamp
        daily_summary.avg_temp = aggregated_data['avg_temp']
        daily_summary.max_temp = aggregated_data['max_temp']
        daily_summary.min_temp = aggregated_data['min_temp']

        # get most dominant weather
        wc = (WeatherUpdate.objects.filter(city=city, created_at__date=date_with_timestamp.date()).values(
            'weather_condition').annotate(count=Count('weather_condition')).order_by('-count').first())
        daily_summary.dominant_weather = wc["weather_condition"] if wc else "Unknown"

    daily_summary.save()
