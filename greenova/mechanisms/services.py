import logging
from typing import Dict, List, Any
from django.db.models import Count
from .models import EnvironmentalMechanism

logger = logging.getLogger(__name__)

class MechanismAnalysisService:
    @staticmethod
    def get_mechanism_distribution(project_id: int, mechanism: str) -> Dict[str, Any]:
        """Calculate distribution data for specified mechanism"""
        try:
            distribution = (EnvironmentalMechanism.objects
                          .filter(project_id=project_id, name=mechanism)
                          .values('status')
                          .annotate(count=Count('id')))

            labels = []
            data = []
            colors = ['#FF6384', '#36A2EB', '#FFCE56']  # Red, Blue, Yellow

            for item in distribution:
                labels.append(item['status'].title())
                data.append(item['count'])

            return {
                'labels': labels,
                'datasets': [{
                    'data': data,
                    'backgroundColor': colors[:len(data)]
                }]
            }

        except Exception as e:
            logger.error(f"Error getting mechanism distribution: {str(e)}")
            raise
