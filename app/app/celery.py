from __future__ import absolute_import
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather_app.settings')

app = Celery('weather_app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Schedule weather fetch every 5 minutes and daily summary at midnight
app.conf.beat_schedule = {
    'fetch-weather-every-5-minutes': {
        'task': 'weather.tasks.fetch_weather_data',
        'schedule': 300.0,  # 5 minutes
    },
    'calculate-daily-summary-midnight': {
        'task': 'weather.tasks.calculate_daily_summary',
        'schedule': 86400.0,  # 24 hours
    },
    'check-alerts-every-5-minutes': {
        'task': 'weather.tasks.check_alerts',
        'schedule': 300.0,  # 5 minutes
    },
}
