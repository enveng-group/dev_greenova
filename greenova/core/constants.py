"""
Constants for the Greenova core app.

This module defines core constants used throughout the Greenova project.
"""

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
THEME_OPTIONS: list[tuple[str, str]] = [
    ("Auto", "auto"),
    ("Light", "light"),
    ("Dark", "dark"),
]

# Footer links
FOOTER_LINKS: list[tuple[str, str, bool]] = [
    ("Enveng Group", "https://www.enveng-group.com.au/", True),
    ("GNU AGPL v3.0", "https://www.gnu.org/licenses/agpl-3.0.html", True),
]
