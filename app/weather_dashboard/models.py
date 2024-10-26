from django.utils.translation import gettext_lazy as _
from django.db import models


class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class WeatherUpdate(models.Model):
    weather_condition = models.CharField(max_length=50)
    temp = models.FloatField(default=0.0)  # In Celsius
    min_temp = models.FloatField(default=0.0)  # In Celsius
    max_temp = models.FloatField(default=0.0)  # In Celsius
    feels_like = models.FloatField(default=0.0)  # In Celsius
    dt = models.IntegerField(default=1729878673)  # Unix timestamp
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='weather_updates')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Weather update for {self.city} at {self.dt}"


class DailySummary(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='daily_summaries')
    date = models.DateTimeField()
    avg_temp = models.FloatField(default=0.0)
    max_temp = models.FloatField(default=0.0)
    min_temp = models.FloatField(default=0.0)
    dominant_weather = models.CharField(max_length=50)

    def __str__(self):
        return f"Daily summary for {self.city} on {self.date}"


class Alert(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    alert_type = models.CharField(max_length=50)
    threshold_value = models.FloatField()
    is_triggered = models.BooleanField(default=False)
    triggered_at = models.DateTimeField(auto_now=True)
    weather_update = models.ForeignKey(WeatherUpdate, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Alert for {self.city}: {self.alert_type} exceeded {self.threshold_value}"


class UserPreference(models.Model):
    class TemperaturePreference(models.TextChoices):
        KELVIN = 'K', _('Kelvin')
        CELSIUS = 'C', _('Celsius')
        FAHRENHEIT = 'F', _('Fahrenheit')

    temp_threshold = models.FloatField(default=35.0)
    temperature_preference = models.CharField(
        max_length=1,
        choices=TemperaturePreference.choices,
        default=TemperaturePreference.CELSIUS.name
    )
    alert_enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"Preferences Temp Threshold{self.temp_threshold}, Preference {self.temperature_preference}"
