from django.core.paginator import Paginator
from django.db.models import QuerySet
from typing import Any

class ProjectPagination:
    """Handle pagination for project-related views."""
    
    def __init__(self, queryset: QuerySet[Any], page_size: int = 10) -> None:
        self.paginator = Paginator(queryset, page_size)
    
    def get_page(self, page_number: int) -> Any:
        """Get the specified page of results."""
        return self.paginator.get_page(page_number)
    
    @property
    def num_pages(self) -> int:
        """Get total number of pages."""
        return self.paginator.num_pages