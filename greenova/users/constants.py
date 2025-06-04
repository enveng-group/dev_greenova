"""constants.py.

Centralized constants for the users app.
"""

USER_ROLE_SUPERUSER = "superuser"
USER_ROLE_STAFF = "staff"
USER_ROLE_REGULAR = "regular"

USER_ROLE_CHOICES = [
    (USER_ROLE_SUPERUSER, "Superuser"),
    (USER_ROLE_STAFF, "Staff"),
    (USER_ROLE_REGULAR, "Regular User"),
]
