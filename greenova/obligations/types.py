from django.db.models.query import QuerySet
from obligations.models import Obligation

ObligationQuerySet = QuerySet[Obligation]
