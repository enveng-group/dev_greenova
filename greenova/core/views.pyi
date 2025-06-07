from _typeshed import Incomplete
from beartype import beartype
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

from .filters import EnvironmentalObligationFilter
from .models import EnvironmentalObligation
from .tables import EnvironmentalObligationTable

logger: Incomplete

class EnvironmentalObligationListView(SingleTableMixin, FilterView):
    model = EnvironmentalObligation
    table_class = EnvironmentalObligationTable
    template_name: str
    filterset_class = EnvironmentalObligationFilter
    context_object_name: str
    @beartype
    def get_queryset(self): ...

@beartype
def obligations_protobuf_api(request: HttpRequest) -> HttpResponse: ...
@beartype
def obligations_api(request: HttpRequest) -> JsonResponse: ...
@beartype
def wasm_theme_api(request: HttpRequest) -> JsonResponse: ...
@beartype
def theme_config_api(request: HttpRequest) -> JsonResponse: ...
@beartype
@login_required
def profile_detail_view(request: HttpRequest) -> HttpResponse: ...
@beartype
@login_required
def profile_edit_view(request: HttpRequest) -> HttpResponse: ...
