# Django-Matplotlib Learning Resources

This guide provides resources for using Matplotlib in Django applications, with a
focus on integrating data visualization into our project.

## Introduction

[Matplotlib](https://matplotlib.org/) is a comprehensive library for creating
static, animated, and interactive visualizations in Python. The
[django-matplotlib](https://pypi.org/project/django-matplotlib/) package provides
specific tools for integrating Matplotlib with Django applications.
[Matplotlib](https://matplotlib.org/) is a comprehensive library for creating static, animated, and interactive visualizations in Python. The [django-matplotlib](https://pypi.org/project/django-matplotlib/) package provides specific tools for integrating Matplotlib with Django applications.

## Installation and Setup

### Basic Installation

```python
# Install the required packages
pip install matplotlib
pip install django-matplotlib
```

### Django Configuration

Add `django_matplotlib` to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ...
    'django_matplotlib',
    # ...
]
```

## Basic Usage

### Creating Charts in Views

```python
from django_matplotlib import MatplotlibMixin
from django.views.generic import TemplateView
import matplotlib.pyplot as plt
import numpy as np

class ChartView(MatplotlibMixin, TemplateView):
    template_name = 'chart_template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Create a figure using matplotlib
        fig, ax = plt.subplots()
        x = np.linspace(0, 2*np.pi, 100)
        y = np.sin(x)
        ax.plot(x, y)
        ax.set_title('Sine Wave')
        ax.set_xlabel('Angle (radians)')
        ax.set_ylabel('Amplitude')

        # Add the figure to the context
        context['chart'] = self.get_png_image(fig)

        return context
```

<h2>Matplotlib Chart Example</h2>
<img src="data:image/png;base64,{{ chart }}" alt="Matplotlib Chart" width="600" height="400" />

```html
<h2>Matplotlib Chart Example</h2>
<img src="data:image/png;base64,{{ chart }}" alt="Matplotlib Chart" />
```

## Alternative Integration Methods

### Direct Image Generation

```python
def generate_chart(request):
    # Create a figure
    fig, ax = plt.subplots()
    # ... plot data ...

    # Convert to HTTP response
    response = HttpResponse(content_type='image/png')
    fig.savefig(response, format='png')
    plt.close(fig)
    return response
```

### Using BytesIO for Template Context

```python
from io import BytesIO
import base64

def chart_view(request):
    # Create a figure
    fig, ax = plt.subplots()
    # ... plot data ...

    # Save to BytesIO object
    buffer = BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    # Encode to base64 string
    graphic = base64.b64encode(image_png).decode('utf-8')

    return render(request, 'template.html', {
        'graphic': graphic
    })
```

## Chart Types and Examples

Django-Matplotlib supports all chart types available in Matplotlib:

- Line charts
- Bar charts
- Pie charts
- Scatter plots
- Histograms
- Box plots
- Heatmaps

## Official Documentation

### Django-Matplotlib

- [PyPI Package](https://pypi.org/project/django-matplotlib/)
- [GitHub Repository](https://github.com/scidam/django_matplotlib)
- [Documentation](https://django-matplotlib.readthedocs.io/en/latest/)

### Matplotlib

- [Main Documentation](https://matplotlib.org/stable/index.html)
- [User Guide](https://matplotlib.org/stable/users/index)
- [Tutorials](https://matplotlib.org/stable/tutorials/index.html)
- [Gallery of Examples](https://matplotlib.org/stable/gallery/index.html)
- [PyPlot Tutorial](https://matplotlib.org/stable/tutorials/pyplot.html)
- [API Reference](https://matplotlib.org/stable/api/index.html)
- [GitHub Repository](https://github.com/matplotlib/matplotlib)

## Tutorials and Guides

### General Matplotlib Tutorials

- [GeeksforGeeks Matplotlib Tutorial](https://www.geeksforgeeks.org/matplotlib-tutorial/)
- [GeeksforGeeks Step-by-Step Guide](https://www.geeksforgeeks.org/matplotlib-step-by-step-guide/)
- [Real Python Matplotlib Guide](https://realpython.com/python-matplotlib-guide/)

### Django Integration Tutorials

- [Matplotlib in Django Templates](https://spapas.github.io/2021/02/08/django-matplotlib/)
- [Adding Matplotlib to Django Templates](https://mdhvkothari.medium.com/matplotlib-into-django-template-5def2e159997)
- [Creating Charts in Django](https://django.cowhite.com/blog/creating-charts-and-output-them-as-images-to-the-browser-in-django-using-python-matplotlib-library/)

## Best Practices

1. **Keep chart generation code separate** from view logic when possible
2. **Cache charts** for improved performance, especially with complex visualizations
3. **Use appropriate chart types** for your data
4. **Consider responsive alternatives** for interactive dashboards (Chart.js, D3.js)
5. **Close figures** with `plt.close(fig)` to prevent memory leaks

## Project-Specific Examples

### 14-Day Lookahead Chart

```python
def generate_lookahead_chart(obligations):
    fig, ax = plt.subplots(figsize=(10, 6))

    # Group by date
    dates = []
    counts = []
    # Process obligation data...

    ax.bar(dates, counts)
    ax.set_title('14-Day Obligation Lookahead')
    ax.set_xlabel('Date')
    ax.set_ylabel('Number of Obligations')

    # Return encoded image
    buffer = BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    plt.close(fig)

    return image_base64
```

### Obligations Progress Chart

```python
def generate_progress_pie_chart(completed, in_progress, not_started):
    fig, ax = plt.subplots()

    labels = ['Completed', 'In Progress', 'Not Started']
    sizes = [completed, in_progress, not_started]
    colors = ['#4CAF50', '#FFC107', '#F44336']

    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')

    # Return chart as before...
```
