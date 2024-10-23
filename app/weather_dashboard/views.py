from .models import DailySummary
from rest_framework import viewsets
from .serializers import DailySummarySerializer

class DailySummaryViewSet(viewsets.ModelViewSet):
    queryset = DailySummary.objects.all()
    serializer_class = DailySummarySerializer
