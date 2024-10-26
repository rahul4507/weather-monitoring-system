from django.db.models.signals import post_save
from django.dispatch import receiver

from weather_dashboard.models import WeatherUpdate, Alert
from weather_dashboard.weather_alerts import check_and_trigger_alerts


@receiver(post_save, sender=WeatherUpdate)
def trigger_alert_on_weather_update_save(sender, instance, **kwargs):
    check_and_trigger_alerts(instance)
