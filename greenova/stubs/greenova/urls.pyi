from _typeshed import Incomplete
from django.http import HttpRequest, HttpResponse

def home_router(request: HttpRequest) -> HttpResponse: ...
def trigger_error(request: HttpRequest) -> HttpResponse: ...

urlpatterns: Incomplete
