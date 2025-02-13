import logging
from typing import Any
from functools import wraps
from time import time

logger = logging.getLogger(__name__)

def log_action(action_name: str):
    """Decorator to log method execution time and status."""
    def decorator(func: Any):
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any):
            start_time = time()
            try:
                result = func(*args, **kwargs)
                logger.info(
                    f"{action_name} completed successfully in {time() - start_time:.2f}s"
                )
                return result
            except Exception as e:
                logger.error(
                    f"{action_name} failed after {time() - start_time:.2f}s: {str(e)}"
                )
                raise
        return wrapper
    return decorator