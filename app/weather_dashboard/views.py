import json
import time

from django.conf import settings
from django.db.models import F
from django.utils.datetime_safe import datetime
from django.views.decorators.cache import cache_control
from django.http import StreamingHttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from .models import DailySummary
from .serializers import DailySummarySerializer


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
