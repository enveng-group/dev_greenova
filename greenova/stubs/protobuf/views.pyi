from django.http import HttpResponse, JsonResponse
from django.views import View

class ProtobufProjectAPIView(View):
    def get(self, request, project_id: int | None = None) -> HttpResponse: ...

class ProtobufObligationAPIView(View):
    def get(self, request, project_id: int) -> HttpResponse: ...

class ProtobufChartDataAPIView(View):
    def get(self, request, chart_id: int) -> HttpResponse: ...

class ProtobufJSONAPIView(View):
    def get(self, request, model_type: str, object_id: int | None = None) -> JsonResponse: ...
