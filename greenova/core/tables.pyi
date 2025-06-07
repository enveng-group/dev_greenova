import django_tables2 as tables
from _typeshed import Incomplete

from .models import EnvironmentalObligation

class EnvironmentalObligationTable(tables.Table):
    class Meta:
        model = EnvironmentalObligation
        template_name: str
        fields: Incomplete
