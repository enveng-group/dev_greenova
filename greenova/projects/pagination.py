from django.core.paginator import Paginator
from django.db.models import QuerySet
from typing import Any
import logging

logger = logging.getLogger(__name__)

class ProjectPagination:
    """Handle pagination for project-related views."""
    
    def __init__(self, queryset: QuerySet[Any], page_size: int = 10) -> None:
        self.paginator = Paginator(queryset, page_size)
    
    def get_page(self, page_number: int) -> Any:
        """Get the specified page of results."""
        try:
            logger.debug(f"Getting page {page_number}")
            return self.paginator.get_page(page_number)
        except Exception as e:
            logger.error(f"Pagination error: {str(e)}")
            raise
    
    @property
    def num_pages(self) -> int:
        """Get total number of pages."""
        return self.paginator.num_pages