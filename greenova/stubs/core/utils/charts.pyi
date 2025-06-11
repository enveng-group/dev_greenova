from collections.abc import Sequence
from matplotlib.figure import Figure

def create_pie_chart(data: Sequence[int], labels: Sequence[str], colors: Sequence[str], title: str = 'Status Distribution', fig_size: tuple[int, int] = (320, 240)) -> Figure: ...
