from typing import List, Tuple

# Main navigation structure
# Format: (name, url_name, icon_class)
MAIN_NAVIGATION: List[Tuple[str, str, str]] = [
    ('Dashboard', 'dashboard:home', 'dashboard-icon'),
    ('Projects', 'projects:select', 'projects-icon'),
    ('Obligations', 'obligations:list', 'obligations-icon'),
    ('Mechanisms', 'mechanisms:list', 'mechanisms-icon'),
    ('Procedures', 'procedures:list', 'procedures-icon'),
]

# User account navigation
USER_NAVIGATION: List[Tuple[str, str, str]] = [
    ('Profile', 'users:profile', 'user-icon'),
    ('Change Password', 'account_change_password', 'key-icon'),
    ('Logout', 'account_logout', 'logout-icon'),
]

# Authentication navigation for anonymous users
AUTH_NAVIGATION: List[Tuple[str, str, str]] = [
    ('Register', 'account_signup', 'register-icon'),
    ('Login', 'account_login', 'login-icon'),
]

# Theme options
THEME_OPTIONS = [
    ('Auto', 'auto'),
    ('Light', 'light'),
    ('Dark', 'dark'),
]

# Footer links
FOOTER_LINKS: List[Tuple[str, str, bool]] = [
    ('Enveng Group', 'https://www.enveng-group.com.au/', True),
    ('GNU AGPL v3.0', 'https://www.gnu.org/licenses/agpl-3.0.html', True),
]
