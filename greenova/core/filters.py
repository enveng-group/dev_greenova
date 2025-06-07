"""FilterSet for EnvironmentalObligation using django-filter.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

# Copyright (c) 2025 Adrian Gallo <agallo@enveng-group.com.au>
# SPDX-License-Identifier: AGPL-3.0

import django_filters

from .models import EnvironmentalObligation


class EnvironmentalObligationFilter(django_filters.FilterSet):
    """FilterSet for filtering EnvironmentalObligation objects."""

    class Meta:
        model = EnvironmentalObligation
        fields = {
            "name": ["icontains"],
            "due_date": ["exact", "gte", "lte"],
            "is_complete": ["exact"],
        }
