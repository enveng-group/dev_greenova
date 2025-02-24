from typing import Dict, Any

class ChartService:
    @staticmethod
    def get_chart_config(chart_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate standardized chart configuration"""
        return {
            "type": chart_type,
            "data": data,
            "options": {
                "responsive": True,
                "maintainAspectRatio": False,
                "plugins": {
                    "legend": {"position": "bottom"}
                }
            }
        }

    @staticmethod
    def get_polar_area_config(data: Dict[str, Any]) -> Dict[str, Any]:
        """Specific configuration for polar area charts"""
        return {
            "type": "polarArea",
            "data": data,
            "options": {
                "responsive": True,
                "maintainAspectRatio": False,
                "plugins": {
                    "legend": {
                        "position": "right",
                        "labels": {
                            "padding": 20,
                            "usePointStyle": True
                        }
                    },
                    "tooltip": {
                        "enabled": True
                    }
                },
                "scales": {
                    "r": {
                        "ticks": {
                            "beginAtZero": True
                        }
                    }
                }
            }
        }
