# GitHub Copilot Instructions for Django Development with POSIX-Compliant Python

This document provides guidelines to configure GitHub Copilot to generate code that is:

- Compliant with HTML-first web development principles.
   - Templates should use semantic HTML first
   - Progressive enhancement layers: HTML → CSS → HTMX → Web APIs → JS
   - Data attributes should be used for behavior
   - Forms should work without JS
- Follows a data-oriented programming paradigm.
- Modular, reusable, and adheres to best practices for Django applications.
Semantic HTML structure:
Proper heading hierarchy (h1, h2, etc.)
Semantic elements (main, article, section, etc.)
ARIA labels and roles
Proper form structure
Progressive Enhancement:
Base functionality works without JS
HTMX attributes for dynamic updates
Proper CSRF token handling
Proper event triggers and indicators
Django-HTMX Integration:
Using hx-get for AJAX requests
Proper event handling
Swap targets and indicators
URL pushing for history
Django-Chartjs Integration:
Using proper template tags
Responsive configurations
Chart containers with proper sizing
Accessibility:
ARIA labels
Proper heading structure
Form labels
Keyboard navigation support

## General Instructions

### Code Style

1. Adhere to PEP 8 standards for Python code:
   - Use 4 spaces per indentation level.
   - Limit lines to a maximum of 79 characters.
   - Include blank lines to separate top-level function and class definitions.

2. Use `snake_case` for function and variable names, `CamelCase` for class names, and `UPPER_CASE` for constants.

3. Place all imports at the top of the file, grouped as:
   - Standard library imports.
   - Third-party library imports.
   - Local application/library-specific imports.

### Comments and Documentation

1. Use comments to explain why the code exists, not what it does.

2. Write docstrings for all public modules, functions, classes, and methods using triple quotes.

3. Ensure inline comments are concise and placed at least two spaces away from the statement.

### Logging

1. Use the `logging` module instead of print statements.

2. Choose appropriate logging levels (DEBUG, INFO, WARNING, ERROR, CRITICAL).

3. Configure logs with timestamps and ensure efficient log file management.

### Virtual Environments

1. Use `venv` or `virtualenv` to create isolated environments for each project.

2. Include a `pyproject.toml` file and `requirements.txt` for dependency management with `pip`.

## Code Generation Workflow

### 1. Initialization

- Initialize Django applications and settings.
- Load configuration data and initialize logging.
- Define transparent, generic data structures.
- Handle exceptions using `try-except` blocks.

### 2. Get Transaction Data

- Retrieve transaction items from input sources like queues or databases.
- Separate data from logic by implementing stateless functions.
- Ensure data is immutable once created.

### 3. Process Transaction

- Process each transaction item using a pipeline of side-effect-free functions.
- Validate data at each step and handle invalid data gracefully.
- Log transaction statuses.

### 4. End Process

- Perform cleanup activities and close applications.
- Log the end of the process.

## POSIX Compliance Guidelines

### Standard Libraries

1. Prefer Python’s standard libraries designed for portability and POSIX compliance.

2. Use modules like `os`, `shutil`, and `subprocess` for system operations.

3. Avoid Windows-specific functions like `os.startfile()`.

### File and Directory Operations

1. Use `os.path` or `pathlib` for path handling.

2. Access and modify environment variables using `os.environ`.

### Process Management

1. Use the `subprocess` module for creating and managing processes.

2. Avoid using `os.system()` for security and flexibility reasons.

### Error Handling

1. Handle exceptions using `try-except` blocks.

2. Ensure resource cleanup with `finally` or context managers.

### Text Encoding

1. Use UTF-8 encoding for text files.

2. Explicitly handle text encoding and decoding with `str.encode()` and `str.decode()`.

### Testing on POSIX Systems

1. Test code on multiple POSIX-compliant systems (e.g., Linux, macOS).

2. Use CI tools to automate testing across environments.

## Django-Specific Guidelines

### Environment Variable Management

1. Always store environment variables in the appropriate files:
   - `.greenova.env`
   - Python shell configuration: `.pythonstartup`

2. When adding new features that require environment variables:
   - Add variables to both environment files
   - Document the purpose and expected format of each variable
   - Use descriptive naming conventions (e.g., `SERVICE_NAME_VARIABLE_PURPOSE`)

3. Environment variable access:
   - Use `os.environ.get()` with a default value for non-critical variables
   - Use `os.environ[]` for required variables
   - Consider creating a settings validation function for critical variables

4. Configuration loading:
   - Use Django's settings module to centralize environment variable loading
   - Create separate settings files for different environments
   - Validate environment variables during application startup

### Settings and Configuration

1. Use environment variables to manage sensitive information (e.g., `os.environ`).
   ```python
   # Example of proper environment variable usage
   SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
   DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'
   ```

2. Follow Django's settings module structure for organization.

3. Ensure all environment-dependent configurations are externalized.

### Models

1. Define models with clear field definitions and constraints.

2. Use migrations to manage database schema changes.

### Views

1. Use class-based views for reusable and modular code.

2. Separate logic from templates by keeping views focused on data preparation.

### Templates

1. Use Django’s template language for rendering HTML.

2. Avoid embedding logic in templates.

### Forms

1. Use Django’s forms framework for input validation and handling.

2. Keep form-related logic in the form classes.

### Middleware

1. Write middleware to handle cross-cutting concerns (e.g., authentication, logging).

2. Ensure middleware adheres to Django’s lifecycle and compatibility.

### Application Testing

1. Write unit tests for views, models, and forms.

2. Use Django’s testing framework for integration tests.

3. Mock external dependencies to isolate test cases.

### Deployment

1. Use POSIX-compliant tools for deployment (e.g., `gunicorn`, `nginx`).

2. Ensure the application runs in a virtual environment.

3. Use environment variables for configuration in production.

## Modular Design Principles

### Core Functionalities

1. Break down applications into independent modules.

2. Define clear interfaces for each module.

### Reusability

1. Write reusable functions and classes.

2. Avoid tightly coupling modules.

### Documentation

1. Document each module’s purpose and usage.

2. Include docstrings for all public components.

### Testing

1. Write unit tests for each module.

2. Use mocking to isolate dependencies.

### Packaging

1. Organize modules into packages with logical structures.

2. Include an `__init__.py` file in each package.

### SQL Schema for Database

```sql
-- Create the obligations table
CREATE TABLE Obligations (
    obligation__number INT PRIMARY KEY,
    project__name VARCHAR(255),
    primary__environmental__mechanism TEXT,
    procedure TEXT,
    environmental__aspect TEXT,
    obligation TEXT,
    accountability INT,
    responsibility INT,
    project_phase TEXT,
    action__due_date DATE,
    close__out__date DATE,
    status VARCHAR(50),
    supporting__information TEXT,
    general__comments TEXT,
    compliance__comments TEXT,
    non_conformance__comments TEXT,
    evidence TEXT,
    person_email TEXT,
    recurring__obligation BOOLEAN,
    recurring__frequency VARCHAR(50),
    recurring__status VARCHAR(50),
    recurring__forcasted__date DATE,
    inspection BOOLEAN,
    inspection__frequency VARCHAR(50),
    site_or__desktop VARCHAR(50),
    new__control__action_required BOOLEAN,
    obligation_type VARCHAR(50),
    gap__analysis TEXT,
    notes_for__gap__analysis TEXT,
    covered_in_which_inspection_checklist TEXT
);
```

## User Journey

### Develop the Landing Page
   - Create a basic homepage template with welcome message, navigation links, and information about the app.
   - Add sections like social media links, testimonials, and FAQ.

### Create the Login Page
   - Implement the login form with handling for both successful and unsuccessful logins.
   - Set up password reset functionality.

### Develop the Dashboard
   - Create a dashboard view displaying user activity, notifications, and quick links.
   - Add a logout feature that redirects to the landing home page.

### Implement User Profile Management
   - Create views for viewing and editing user profiles.
   - Implement CRUD operations for updating user information, changing passwords, and uploading profile pictures.

### Set Up Admin Panel for User Management
   - Enable Django’s admin interface to manage users, assign roles, and perform CRUD operations.

### Set Up Auditing for User Changes
   - Implement logging for user actions (e.g., changes to profiles, user deletions).
   - Use Django's built-in logging system.

### Create Dynamic Charts for Project Database Records
   - Implement basic data visualizations for 14-day lookahead, overdue obligations, and obligations progress.
   - Provide CRUD operations for managing database records.

### Create Additional Features
   - Implement help sections (e.g., FAQ).
   - Add account settings and notification preferences.
   - Implement feedback forms for user input.

## Toolchain Instructions

### Toolchain

1. **Django**: Backend framework.
2. **SQLite3**: Lightweight database for development and production.
3. **Docker**: Containerization platform.
4. **GitHub CI/CD**: Continuous integration and deployment.
5. **django-htmx**: Python wrapper for HTMX
6. **django-chartjs**: Chart.js wrapper for python

### Step-by-Step Instructions

1. **Set Up Environment**:
   - Install Python, SQLite3, and Docker.
   - Create a virtual environment using `python -m venv env`.

2. **Initialize Django Project**:
   - Run `django-admin startproject project_name`.
   - Set up the database connection in `settings.py` to use SQLite3.

3. **Create Database Schema**:
   - Use the Django ORM to define models based on the provided SQL schema for the obligations table.
   - Run `python manage.py makemigrations` to generate migrations.
   - Run `python manage.py migrate` to apply the schema to the SQLite3 database.

4. **Develop the Landing Page**:
   - Create a new app using `python manage.py startapp landing`.
   - Add the app to `INSTALLED_APPS` in `settings.py`.
   - Define a `LandingPageView` class in `views.py` and create a corresponding template.
   - Use HTMX to add interactivity for sections like FAQs or testimonials.

5. **Create the Login Page**:
   - Use Django’s built-in authentication system.
   - Create a `LoginView` and customize the template for user-friendly design.
   - Add password reset views and templates.

6. **Develop the Dashboard**:
   - Create a `DashboardView` in a new app (e.g., `dashboard`).
   - Fetch and display user-specific data using Django ORM.
   - Add logout functionality by linking to Django's `LogoutView`.

7. **Implement User Profile Management**:
   - Add a `UserProfile` model to store additional user information.
   - Create views and forms for profile editing, password changes, and profile picture uploads.

8. **Set Up the Admin Panel**:
   - Customize the Django admin interface for managing users and obligations.
   - Use `@admin.register` to register models with custom configurations.

9. **Set Up Auditing**:
    - Use Django’s logging framework to log user actions.
    - Add middleware or signal handlers to track changes and write logs.

10. **Create Dynamic Charts**:
    - Use Chart.js for visualizations in the dashboard.
    - Pass data to templates using Django context or AJAX calls with HTMX.

11. **Add Additional Features**:
    - Implement a help section using static pages.
    - Create account settings and notification preferences views.
    - Add feedback forms using Django’s forms framework.

