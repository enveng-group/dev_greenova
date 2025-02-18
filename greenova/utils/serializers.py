from typing import Dict, Any, List

class ChartDataSerializer:
    """Serialize data for chart rendering."""
    
    @staticmethod
    def format_mechanism_data(data: Dict[str, List[Any]]) -> Dict[str, Any]:
        """Format mechanism chart data."""
        return {
            'type': 'doughnut',
            'data': {
                'labels': data['labels'],
                'datasets': [{
                    'data': data['values'],
                    'backgroundColor': data['colors']
                }]
            },
            'options': {
                'responsive': True,
                'maintainAspectRatio': True
            }
        }

    @staticmethod
    def format_trend_data(
        data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Format trend chart data."""
        dates = sorted(set(
            item['action_due_date'] for item in data
        ))
        
        datasets: List[Dict[str, Any]] = []
        for status in ['not started', 'in progress', 'completed']:
            status_data: List[int] = []
            for date in dates:
                count = sum(
                    item['count']
                    for item in data
                    if item['action_due_date'] == date
                    and item['status'] == status
                )
                status_data.append(count)
            
            datasets.append({
                'label': status.title(),
                'data': status_data
            })
            
        return {
            'type': 'line',
            'data': {
                'labels': [
                    d.strftime('%Y-%m-%d')
                    for d in dates
                ],
                'datasets': datasets
            }
        }