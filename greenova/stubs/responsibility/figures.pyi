from _typeshed import Incomplete
from matplotlib.figure import Figure

logger: Incomplete

def generate_responsibility_chart(responsibility_counts: dict[str, int], fig_width: int = 600, fig_height: int = 300) -> Figure: ...
def get_responsibility_chart(mechanism_id: int, fig_width: int = 600, fig_height: int = 300, filtered_ids: list[int] | None = None) -> Figure: ...
