"""constants.py.

Centralized constants for the projects app.
"""

# Project role choices
ROLE_OWNER = "owner"
ROLE_MANAGER = "manager"
ROLE_MEMBER = "member"
ROLE_VIEWER = "viewer"

PROJECT_ROLE_CHOICES = [
    (ROLE_OWNER, "Owner"),
    (ROLE_MANAGER, "Manager"),
    (ROLE_MEMBER, "Member"),
    (ROLE_VIEWER, "Viewer"),
]
