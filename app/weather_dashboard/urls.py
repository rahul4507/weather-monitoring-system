from django.urls import path

from .views import DailyWeatherSummaryView

app_name = "users"

urlpatterns = [
    path('weather/daily-summary/stream', DailyWeatherSummaryView.as_view(), name='daily_weather_summary'),
    # path('weather/alerts/stream/', sse_alert_stream, name='sse_alert_stream'),
]
