"""Pytest test cases for figures.py in mechanisms app."""

from beartype import beartype
from mechanisms import figures

PIE_LABELS: list[str] = ["Not Started", "In Progress", "Completed"]
PIE_COLORS: list[str] = ["#f9c74f", "#90be6d", "#43aa8b"]


@beartype
def test_generate_plotly_pie_chart_basic() -> None:
    """
    Test that generate_plotly_pie_chart returns valid HTML for basic input.

    Asserts that the returned HTML contains the expected labels and is a string.
    """
    data: list[int] = [10, 20, 30]
    html: str = figures.generate_plotly_pie_chart(
        data, PIE_LABELS, PIE_COLORS, mechanism_id=1, chart_title="Test Chart"
    )
    assert isinstance(html, str)
    assert "plotly" in html or "<div" in html
    for label in PIE_LABELS:
        assert label in html


@beartype
def test_generate_plotly_pie_chart_empty() -> None:
    """
    Test that generate_plotly_pie_chart handles empty input gracefully.

    Asserts that the returned HTML is a string and contains a div.
    """
    data: list[int] = []
    labels: list[str] = []
    colors: list[str] = []
    html: str = figures.generate_plotly_pie_chart(data, labels, colors)
    assert isinstance(html, str)
    assert "plotly" in html or "<div" in html
