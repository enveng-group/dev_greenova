from typing import Any

from _typeshed import Incomplete
from beartype import beartype
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    TemplateView,
    UpdateView,
)

from .filters import ObligationFilter as ObligationFilter
from .forms import EvidenceUploadForm as EvidenceUploadForm
from .forms import ObligationForm as ObligationForm
from .forms import ResponsibilityAssignmentFormSet as ResponsibilityAssignmentFormSet
from .mixins import ObligationContextMixin as ObligationContextMixin
from .mixins import (
    ObligationPermissionRequiredMixin as ObligationPermissionRequiredMixin,
)
from .models import Obligation as Obligation
from .models import ObligationEvidence as ObligationEvidence
from .serializers import (
    ObligationCollectionProtoSerializer as ObligationCollectionProtoSerializer,
)
from .serializers import ObligationProtoSerializer as ObligationProtoSerializer
from .tables import get_obligation_table as get_obligation_table
from .utils import is_obligation_overdue as is_obligation_overdue

logger: Incomplete

class ObligationSummaryView(LoginRequiredMixin, ObligationContextMixin, TemplateView):
    template_name: str
    @beartype
    def get_template_names(self) -> list[str]: ...
    @beartype
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]: ...

class TotalOverdueObligationsView(
    LoginRequiredMixin, ObligationPermissionRequiredMixin, View
):
    @beartype
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> JsonResponse: ...

class ObligationCreateView(
    LoginRequiredMixin,
    ObligationPermissionRequiredMixin,
    ObligationContextMixin,
    CreateView,
):
    model = Obligation
    form_class = ObligationForm
    template_name: str
    @beartype
    def get_form_kwargs(self) -> dict[str, Any]: ...
    @beartype
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]: ...
    @beartype
    def form_valid(self, form: Any) -> HttpResponse: ...
    @beartype
    def form_invalid(self, form: Any) -> HttpResponse: ...

class ObligationDetailView(
    LoginRequiredMixin,
    ObligationPermissionRequiredMixin,
    ObligationContextMixin,
    DetailView,
):
    model = Obligation
    template_name: str
    context_object_name: str
    pk_url_kwarg: str
    @beartype
    def user_has_role(self, roles: list[str]) -> bool: ...
    @beartype
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]: ...

class ObligationUpdateView(
    LoginRequiredMixin,
    ObligationPermissionRequiredMixin,
    ObligationContextMixin,
    UpdateView,
):
    model = Obligation
    form_class = ObligationForm
    template_name: str
    slug_field: str
    slug_url_kwarg: str
    object: Incomplete
    @beartype
    def dispatch(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse: ...
    @beartype
    def get_template_names(self) -> list[str]: ...
    @beartype
    def get_form_kwargs(self) -> dict[str, Any]: ...
    @beartype
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]: ...
    @beartype
    def form_valid(self, form: Any) -> HttpResponse: ...
    @beartype
    def form_invalid(self, form: Any) -> HttpResponse: ...

class ObligationDeleteView(
    LoginRequiredMixin, ObligationPermissionRequiredMixin, DeleteView
):
    model = Obligation
    pk_url_kwarg: str
    object: Incomplete
    @beartype
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> JsonResponse: ...

class ToggleCustomAspectView(View):
    @beartype
    def get(self, request: HttpRequest) -> HttpResponse: ...

@beartype
def upload_evidence(
    request: HttpRequest, obligation_id: int
) -> HttpResponse | None: ...
@beartype
@login_required
def export_obligation(request: HttpRequest, obligation_number: str) -> HttpResponse: ...
@beartype
@login_required
def export_all_obligations(request: HttpRequest) -> HttpResponse: ...
@beartype
@login_required
def import_obligation(request: HttpRequest) -> HttpResponse: ...

class ObligationListView(LoginRequiredMixin, ObligationContextMixin, TemplateView):
    template_name: str
    @beartype
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]: ...
    def render_to_response(
        self, context: dict[str, Any], **response_kwargs: Any
    ) -> HttpResponse: ...
