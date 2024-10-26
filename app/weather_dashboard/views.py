import json
import time

from django.conf import settings
from django.db.models import F
from django.utils.datetime_safe import datetime
from django.views.decorators.cache import cache_control
from django.http import StreamingHttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from .models import DailySummary, Alert, WeatherUpdate, City, UserPreference
from .serializers import DailySummarySerializer, WeatherUpdateSerializer


class DailyWeatherSummaryView(View):
    @method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True))
    def get(self, request):
        response = StreamingHttpResponse(self.event_stream(), content_type='text/event-stream')
        response['Cache-Control'] = 'no-cache'
        return response

    def event_stream(self):
        while True:
            summaries = (DailySummary.objects.filter(date__date=datetime.now().date()).
                         annotate(city_name=F('city__name')))
            serialized_summaries = DailySummarySerializer(summaries, many=True)
            event_data = {'daily_summaries': serialized_summaries.data}
            yield f"data: {json.dumps(event_data)}\n\n"

            time.sleep(settings.SSE_DELAY)


class WeatherUpdateStreamView(View):
    @method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True))
    def get(self, request):
        response = StreamingHttpResponse(self.event_stream(), content_type='text/event-stream')
        response['Cache-Control'] = 'no-cache'
        return response

    def event_stream(self):
        while True:
            # Get the latest 10 weather updates
            latest_updates = WeatherUpdate.objects.order_by('created_at')[:300]
            serialized_updates = WeatherUpdateSerializer(latest_updates, many=True).data  # Serialize the updates
            event_data = {'weather_updates': serialized_updates}

            yield f"data: {json.dumps(event_data)}\n\n"
            time.sleep(settings.SSE_DELAY)  # Use your configured delay

class AlertThresholdsView(View):
    @method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True))
    def get(self, request):
        response = StreamingHttpResponse(self.event_stream(), content_type='text/event-stream')
        response['Cache-Control'] = 'no-cache'
        return response

    def event_stream(self):
        last_alert_id = None  # Keep track of the last alert ID sent
        consecutive_updates = 2  # Number of consecutive updates for threshold breach

        # Retrieve user preferences
        # try:
        #     user_preferences = UserPreference.objects.get(user=user)
        #     threshold_temp = user_preferences.temp_threshold
        # except UserPreference.DoesNotExist:
        threshold_temp = 100  # Default threshold if user preference is not set

        consecutive_count = 0  # Counter for consecutive updates
        while True:
            # Get the latest daily summaries for today
            daily_summaries = (
                DailySummary.objects.filter(date__date=datetime.now().date())
                .annotate(city_name=F('city__name'))
            )
            serialized_summaries = DailySummarySerializer(daily_summaries, many=True)

            # Check for temperature breaches
            for summary in serialized_summaries.data:
                avg_temp = summary.get('avg_temp')
                city_name = summary.get('city_name')

                if avg_temp > threshold_temp:
                    consecutive_count += 1
                    if consecutive_count >= consecutive_updates:
                        # Check if an alert is already triggered for this city
                        alert, created = Alert.objects.get_or_create(
                            city=City.objects.get(name=city_name),
                            alert_type='Temperature Alert',
                            threshold_value=threshold_temp,
                            defaults={'is_triggered': True}
                        )
                        if created or not alert.is_triggered:
                            alert.is_triggered = True
                            alert.weather_update = WeatherUpdate.objects.filter(
                                city__name=city_name).last()  # Get the latest weather update
                            alert.save()

                            alert_message = f"Alert: Temperature in {city_name} exceeded {threshold_temp}°C for {consecutive_updates} consecutive updates."
                            yield f"data: {alert_message}\n\n"
                else:
                    consecutive_count = 0  # Reset counter if threshold not breached

            # Prepare daily summaries for the SSE stream
            event_data = {'daily_summaries': serialized_summaries.data}
            yield f"data: {json.dumps(event_data)}\n\n"

            time.sleep(settings.SSE_DELAY)  # Use your configured delay
