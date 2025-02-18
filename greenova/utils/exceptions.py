from typing import Optional

class GreenovaException(Exception):
    """Base exception for all Greenova-specific exceptions."""
    def __init__(self, message: str, code: Optional[str] = None) -> None:
        self.message = message
        self.code = code
        super().__init__(self.message)

class ProjectError(GreenovaException):
    """Raised when there's an error with project operations."""
    pass

class ObligationError(GreenovaException):
    """Raised when there's an error with obligation operations."""
    pass

class ChartDataError(GreenovaException):
    """Raised when there's an error processing chart data."""
    pass

class DashboardError(GreenovaException):
    """Dashboard-specific errors."""
    pass