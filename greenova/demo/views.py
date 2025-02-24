from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import pandas as pd
from typing import Dict, Any

def demo_charts(request: HttpRequest) -> HttpResponse:
    """Render demo charts view with mechanism status data."""
    # Read CSV
    df: pd.DataFrame = pd.read_csv('clean_output_with_nulls.csv')

    # Group by mechanism and status, count occurrences
    status_counts: pd.DataFrame = df.groupby(['primary__environmental__mechanism', 'status']).size().unstack(fill_value=0)

    # Prepare data for Chart.js
    chart_data: Dict[str, Any] = {
        'labels': status_counts.index.tolist(),
        'datasets': [{
            'data': status_counts['not started'].tolist(),
            'label': 'Not Started',
            'backgroundColor': 'rgba(255, 99, 132, 0.5)'
        }, {
            'data': status_counts['in progress'].tolist(),
            'label': 'In Progress',
            'backgroundColor': 'rgba(54, 162, 235, 0.5)'
        }, {
            'data': status_counts['completed'].tolist(),
            'label': 'Completed',
            'backgroundColor': 'rgba(255, 205, 86, 0.5)'
        }]
    }

    return render(request, 'demo/charts.html', {'chart_data': chart_data})
