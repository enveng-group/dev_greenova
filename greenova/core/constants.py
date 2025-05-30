"""Copyright (C) 2025 Adrian Gallo.

This file is part of Greenova.

Greenova is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Greenova is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with Greenova. If not, see <https://www.gnu.org/licenses/>.

Author: Adrian Gallo <agallo@enveng-group.com.au>
"""

"""Constants for the Greenova core app.

This module defines core constants used throughout the Greenova project.
"""

MAIN_NAVIGATION: list[tuple[str, str, str]] = [
    ("Dashboard", "dashboard:home", "dashboard-icon"),
    ("Projects", "projects:select", "projects-icon"),
    ("Obligations", "obligations:list", "obligations-icon"),
    ("Mechanisms", "mechanisms:list", "mechanisms-icon"),
    ("Procedures", "procedures:list", "procedures-icon"),
]

USER_NAVIGATION: list[tuple[str, str, str]] = [
    ("Profile", "users:profile", "user-icon"),
    ("Change Password", "account_change_password", "key-icon"),
    ("Logout", "account_logout", "logout-icon"),
]

AUTH_NAVIGATION: list[tuple[str, str, str]] = [
    ("Register", "account_signup", "register-icon"),
    ("Login", "account_login", "login-icon"),
]

THEME_OPTIONS: list[tuple[str, str]] = [
    ("Auto", "auto"),
    ("Light", "light"),
    ("Dark", "dark"),
]

FOOTER_LINKS: list[tuple[str, str, bool]] = [
    ("Enveng Group", "https://www.enveng-group.com.au/", True),
    ("GNU AGPL v3.0", "https://www.gnu.org/licenses/agpl-3.0.html", True),
]
