from django.db import models

class City(models.Model):
    name = models.CharField(max_length=100)

class WeatherUpdate(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    temp = models.FloatField()  # In Celsius
    feels_like = models.FloatField()
    weather_condition = models.CharField(max_length=50)
    timestamp = models.DateTimeField()

class DailySummary(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    date = models.DateField()
    avg_temp = models.FloatField()
    max_temp = models.FloatField()
    min_temp = models.FloatField()
    dominant_weather = models.CharField(max_length=50)
