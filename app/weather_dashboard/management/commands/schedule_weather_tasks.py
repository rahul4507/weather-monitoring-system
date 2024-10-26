from django.conf import settings
from django.core.management.base import BaseCommand
from django_q.tasks import schedule, Schedule


class Command(BaseCommand):
    help = 'Schedule weather data fetching tasks'

    def handle(self, *args, **kwargs):
        print(f"Scheduled fetch weather data task at every {settings.INTERVAL} minutes...")
        schedule(
            'weather_dashboard.tasks.fetch_weather_data_task',
            schedule_type=Schedule.MINUTES,
            minutes=settings.INTERVAL,
        )
