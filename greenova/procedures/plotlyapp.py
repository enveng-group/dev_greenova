# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: 	AGPL-3.0-or-later

# This is the interactive plotting library we're going to use!
import plotly.express as px

# pio.renderers.default = 'browser'  # Set default renderer to browser
from dash import dcc, html  # uv pip install dash
from django_plotly_dash import DjangoDash

# Sample data
data = {
    "Category": ["Apples", "Bananas", "Cherries", "Dates"],
    "Values": [25, 35, 20, 20],
}

fig = px.pie(
    data,
    names=data["Category"],
    values=data["Values"],
    title="Fruit Distribution")

# Create instance of DjangoDash
app = DjangoDash("SimpleApp")
app.layout = html.Div([
    html.H1("Simple Dash App"),
    dcc.Graph(
        id="example-graph",
        figure=fig.to_html(),
    ),
    html.Div(id="output-container"),
])
