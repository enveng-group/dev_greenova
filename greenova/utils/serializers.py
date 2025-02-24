from typing import Dict, Any, List, TypedDict, Union, Sequence, cast


class ChartDataset(TypedDict, total=False):
    data: Sequence[Union[int, float]]
    label: str
    backgroundColor: Sequence[str]


class ChartData(TypedDict):
    type: str
    data: Dict[str, Union[List[str], List[ChartDataset]]]


class ChartDataSerializer:
    """Serialize data for chart rendering."""

    @staticmethod
    def format_mechanism_data(data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Format mechanism chart data."""
        return {
            'type': 'polarArea',
            'data': {
                'labels': [item['label'] for item in data],
                'datasets': [{
                    'data': [item['value'] for item in data],
                    'backgroundColor': [item['color'] for item in data],
                    'borderColor': 'rgba(255, 255, 255, 0.5)',
                    'borderWidth': 1
                }]
            }
        }

    @staticmethod
    def format_trend_data(data: List[Dict[str, Any]]) -> ChartData:
        """Format trend chart data."""
        dates = sorted(set(
            item['action_due_date'] for item in data
        ))

        datasets: List[ChartDataset] = []
        for status in ['not started', 'in progress', 'completed']:
            status_data: List[int] = []
            for date in dates:
                count = sum(
                    item['count'] for item in data
                    if item['action_due_date'] == date and
                    item['status'] == status
                )
                status_data.append(count)

            dataset: ChartDataset = {
                'label': status.title(),
                'data': cast(Sequence[Union[int, float]], status_data),
                'backgroundColor': []  # Add empty list to satisfy type requirements
            }
            datasets.append(dataset)

        return cast(ChartData, {
            'type': 'line',
            'data': {
                'labels': [date.strftime('%Y-%m-%d') for date in dates],
                'datasets': datasets
            }
        })
