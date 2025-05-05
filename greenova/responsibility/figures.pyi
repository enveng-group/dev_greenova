# Stub file for responsibility.figures
from typing import Dict, List, Optional

from matplotlib.figure import Figure

def generate_responsibility_chart(
    responsibility_counts: Dict[str, int], fig_width: int = ..., fig_height: int = ...
) -> Figure: ...
def get_responsibility_chart(
    mechanism_id: int,
    fig_width: int = ...,
    fig_height: int = ...,
    filtered_ids: Optional[List[int]] = None,
) -> Figure: ...
