from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import DailySummaryViewSet

app_name = "users"
router = DefaultRouter()
router.register(r'weather/daily-summaries/', DailySummaryViewSet, basename='rule')

urlpatterns = [
    path('', include(router.urls)),
]
