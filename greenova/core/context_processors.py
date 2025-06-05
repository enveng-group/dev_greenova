"""Custom context processors for the core app.

Provides global settings and site-wide context for templates.

Returns:
    dict: Context variables for templates.
"""
from typing import Any, Dict
from beartype import beartype

def core_context(request) -> Dict[str, Any]:
    """Inject core/global context variables into templates.

    Args:
        request: The current HttpRequest object.

    Returns:
        A dictionary of core/global context variables.
    """
    # Example: Add global settings, feature flags, etc.
    return {
        # "site_name": ...,
        # "feature_flags": ...,
    }
