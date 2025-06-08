"""utils.py: General-purpose utility functions for the obligations app.

This module is intended for reusable helper functions that improve code
maintainability and clarity. All functions must be type-annotated and use the
@beartype decorator. Follow project standards for documentation and imports.

Existing utility functions should be migrated here as needed.

Note: Status, overdue, and frequency normalization logic is provided by core.utils.
"""

import logging

logger = logging.getLogger(__name__)

# All status, overdue, and frequency normalization logic is provided by core.utils.
# Import and use core.utils functions directly in the obligations app.
