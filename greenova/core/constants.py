from typing import Final

# Main navigation structure
# Format: (name, url_name, icon_class)
MAIN_NAVIGATION: list[tuple[str, str, str]] = [
    ("Dashboard", "dashboard:home", "dashboard-icon"),
    ("Projects", "projects:select", "projects-icon"),
    ("Obligations", "obligations:list", "obligations-icon"),
    ("Mechanisms", "mechanisms:list", "mechanisms-icon"),
    ("Procedures", "procedures:list", "procedures-icon"),
]

# User account navigation
USER_NAVIGATION: list[tuple[str, str, str]] = [
    ("Profile", "users:profile", "user-icon"),
    ("Change Password", "account_change_password", "key-icon"),
    ("Logout", "account_logout", "logout-icon"),
]

# Authentication navigation for anonymous users
AUTH_NAVIGATION: list[tuple[str, str, str]] = [
    ("Register", "account_signup", "register-icon"),
    ("Login", "account_login", "login-icon"),
]

# Theme options
THEME_OPTIONS = [
    ("Auto", "auto"),
    ("Light", "light"),
    ("Dark", "dark"),
]

# Footer links
FOOTER_LINKS: list[tuple[str, str, bool]] = [
    ("Enveng Group", "https://www.enveng-group.com.au/", True),
    ("GNU AGPL v3.0", "https://www.gnu.org/licenses/agpl-3.0.html", True),
    ("Privacy Policy", "https://www.example.com/privacy", True),
    ("Terms of Service", "https://www.example.com/terms", True),
    ("Contact Us", "https://www.example.com/contact", True),
    ("Support", "https://www.example.com/support", True),
    ("Documentation", "https://www.example.com/docs", True),
    ("API Documentation", "https://www.example.com/api-docs", True),
    ("Feedback", "https://www.example.com/feedback", True),
    ("Blog", "https://www.example.com/blog", True),
    ("Careers", "https://www.example.com/careers", True),
    ("Community", "https://www.example.com/community", True),
]

# General status values
STATUS_ACTIVE: Final[str] = "active"
STATUS_INACTIVE: Final[str] = "inactive"
STATUS_PENDING: Final[str] = "pending"
STATUS_ARCHIVED: Final[str] = "archived"
STATUS_CHOICES: Final[list[tuple[str, str]]] = [
    (STATUS_ACTIVE, "Active"),
    (STATUS_INACTIVE, "Inactive"),
    (STATUS_PENDING, "Pending"),
    (STATUS_ARCHIVED, "Archived"),
]

# Yes/No choices
YES: Final[str] = "yes"
NO: Final[str] = "no"
YES_NO_CHOICES: Final[list[tuple[str, str]]] = [
    (YES, "Yes"),
    (NO, "No"),
]

# Priority levels
PRIORITY_LOW: Final[str] = "low"
PRIORITY_MEDIUM: Final[str] = "medium"
PRIORITY_HIGH: Final[str] = "high"
PRIORITY_CHOICES: Final[list[tuple[str, str]]] = [
    (PRIORITY_LOW, "Low"),
    (PRIORITY_MEDIUM, "Medium"),
    (PRIORITY_HIGH, "High"),
]
