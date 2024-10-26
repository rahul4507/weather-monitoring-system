from django.urls import path

from .views import DailyWeatherSummaryView, AlertThresholdsView, WeatherUpdateStreamView

app_name = "users"

urlpatterns = [
    path('weather/daily-summary/stream', DailyWeatherSummaryView.as_view()),
    path('weather/alerts/stream/', AlertThresholdsView.as_view()),
    path('weather-updates/stream/', WeatherUpdateStreamView.as_view()),

]
