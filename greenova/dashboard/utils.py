"""Copyright (C) 2024 Adrian Gallo <agallo@enveng-group.com.au>
This file is part of Greenova and is licensed under the AGPL-3.0.

Dashboard app utilities for Greenova.

Security and sanitization helpers (bleach, permissions).
"""

import bleach
from beartype import beartype


@beartype
def sanitize_html(
    value: str,
    tags: list[str] | None = None,
    attributes: dict[str, list[str]] | None = None,
) -> str:
    """Sanitize HTML input using bleach.

    Args:
        value: The HTML string to sanitize.
        tags: Optional list of allowed HTML tags.
        attributes: Optional dict of allowed attributes per tag.

    Returns:
        The sanitized HTML string.

    """
    allowed_tags = tags or [
        "b",
        "i",
        "u",
        "em",
        "strong",
        "a",
        "ul",
        "ol",
        "li",
        "p",
        "br",
        "span",
    ]
    allowed_attrs = attributes or {"a": ["href", "title", "target"], "span": ["class"]}
    return bleach.clean(
        value,
        tags=allowed_tags,
        attributes=allowed_attrs,
        strip=True,
    )
