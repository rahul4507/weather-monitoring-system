from django.contrib import admin

from .models import WeatherUpdate, City, DailySummary, UserPreference, Alert

admin.site.register(WeatherUpdate)
admin.site.register(City)
admin.site.register(DailySummary)
admin.site.register(UserPreference)
admin.site.register(Alert)
