# GitHub Copilot Instructions for Django Development with Python

## Project Domain

Greenova is a Django web application for environmental management, focusing on
tracking environmental obligations and compliance requirements.

## Technical Stack

We use Python 3.9.21 with Django 4.1.13 for backend development.

Our frontend uses Tailwind CSS as the primary CSS framework.

We implement frontend interactivity with django-hyperscript for simple
interactions and django-htmx for more complex AJAX functionality. Custom
JavaScript is only used as a last resort.

We follow PEP 8 style guidelines with a strict maximum line length of 88
characters for all Python files.

We organize code in a modular Django architecture with specialized apps for
different functional areas.

We use class-based views with mixins for code reuse in Django.

We implement proper model relationships and constraints in our database design.

We handle authentication using django-allauth with multi-factor authentication
support.

## Data Structure

Our primary data model is the Obligation model which tracks environmental
compliance requirements. Obligations are related to Projects, Mechanisms, and
Procedures.

Users are assigned Responsibilities related to Obligations.

Reference: See `/docs/resources/matplotlib.md` for integrating Matplotlib with
Django for data visualization.

- Layer 5: JavaScript as fallback

```html
<div data-widget="datepicker">
  <input type="date" name="start_date" />
  <noscript>Please enter date in YYYY-MM-DD format</noscript>
</div>
```

We enforce code quality with pylint, pylint-django, eslint, djlint, and
markdownlint.

```html
<button
  type="button"
  data-action="filter"
  data-target="results"
  data-param="status=active"
>
  Filter Active
</button>
```

We use mypy with django-stubs for type checking Python code.

```html
<form method="post" action="{% url 'submit' %}" novalidate>
  {% csrf_token %}
  <fieldset>
    <legend>Contact Information</legend>
    <label for="email">Email:</label>
    <input
      type="email"
      id="email"
      name="email"
      required
      aria-describedby="email-help"
    />
    <small id="email-help">We'll never share your email</small>
  </fieldset>
  <button type="submit">Submit</button>
</form>
```

We maintain compatible versions of dependencies:

1. HTML Hierarchy:

   - Proper use of h1-h6 elements
   - Semantic containers (main, article, section)
   - Descriptive ARIA labels and roles
   - Well-structured forms with labels

```html
<main>
  <h1>Page Title</h1>
  <article>
    <header>
      <h2>Article Title</h2>
      <p>Meta information</p>
    </header>
    <section aria-labelledby="section1">
      <h3 id="section1">Section Heading</h3>
      <!-- Content -->
    </section>
  </article>
  <aside role="complementary">
    <h2>Related Information</h2>
    <!-- Sidebar content -->
  </aside>
</main>
```

1. Progressive Enhancement:
   - Base functionality without JavaScript
   - Django-HTMX integration with proper attributes
   - CSRF token handling in forms
   - Clear loading/error indicators

```html
<!-- Base functionality -->
<form method="post" action="{% url 'search' %}">
  {% csrf_token %}
  <input type="search" name="q" />
  <button type="submit">Search</button>
</form>

<!-- HTMX enhancement -->
<div hx-target="#results" hx-swap="innerHTML" hx-include="[name='q']">
  <input
    type="search"
    name="q"
    hx-get="/search"
    hx-trigger="keyup delay:500ms"
  />
  <div id="results" role="region" aria-live="polite"></div>
</div>
```

### Framework Integration

1. -Django-HTMX Requirements:

   - Use hx-get for AJAX requests
   - Implement proper event handlers
   - Define clear swap targets
   - Enable URL history management

2. Matplotlib Implementation:
   - Use Django template tags
   - Implement responsive chart configs
   - Proper sizing of chart containers

### Accessibility Standards

1. Required Elements:

   - ARIA labels for interactive elements
   - Proper heading structure
   - Form labels and descriptions
   - Keyboard navigation support

2. Development Approach:
   - Follow data-oriented programming
   - Create modular, reusable components
   - Adhere to Django best practices

## General Instructions

### Code Style

1. Adhere to PEP 8 standards for Python code:

   - Use 4 spaces per indentation level.
   - Limit lines to a maximum of 79 characters.
   - Include blank lines to separate top-level function and class definitions.

2. Use `snake_case` for function and variable names, `CamelCase` for class
   names, and `UPPER_CASE` for constants.

3. Place all imports at the top of the file, grouped as:
   - Standard library imports.
   - Third-party library imports.
   - Local application/library-specific imports.

### Comments and Documentation

1. Use comments to explain why the code exists, not what it does.
2. Write docstrings for all public modules, functions, classes, and methods
   using triple quotes. Follow Google style docstrings.
3. Ensure inline comments are concise and placed at least two spaces away from
   the statement.

### Logging

1. Use the `logging` module instead of print statements.
2. Choose appropriate logging levels (DEBUG, INFO, WARNING, ERROR, CRITICAL).
3. Use lazy formatting with `%` style or `logging.Formatter` for log messages,
   avoiding f-strings directly in logging calls (prevents `pylint: W1203`).
   Example: `logger.info("Processing item %s", item_id)`
4. Configure logs with timestamps and ensure efficient log file management.

### Virtual Environments

1. Use `venv` or `virtualenv` to create isolated environments for each project.

2. Include a `pyproject.toml` file and `requirements.txt` for dependency
   management.

3. Include a `pyproject.toml` file and `requirements.txt` for dependency
   management with `pip`.

### Text Encoding

1. Use UTF-8 encoding for text files whenever possible.
2. Explicitly handle text encoding and decoding with `str.encode()` and
   `str.decode()`.
3. Always specify `encoding="utf-8"` when using `open()` (prevents
   `pylint: W1514`). Example:
   `with open("file.txt", "r", encoding="utf-8") as f:`

### Testing on POSIX Systems

1. Test code on multiple POSIX-compliant systems (e.g., Linux, macOS).

2. Use CI tools to automate testing across environments.

### Common Linting and Typing Issues (Pylint/MyPy)

Refer to the `.github/.copilot-codeGeneration-instructions.md` and
`.github/.copilot-review-instructions.md` for detailed guidance on avoiding
common errors like:

- **Pylint**: `line-too-long`, `import-outside-toplevel`, `import-error`,
  `logging-fstring-interpolation`, `invalid-str-returned`, `unused-argument`,
  `broad-exception-caught`, `too-many-return-statements`, `no-else-return`,
  `consider-using-max-builtin`, `unnecessary-pass`, `unspecified-encoding`,
  `too-many-ancestors`, `redefined-outer-name`, `unused-variable`.
- **MyPy**: Incompatible imports, name redefinitions, unused type ignores,
  incorrect arguments (`call-arg`), missing type annotations
  (`no-untyped-def`).

Strict adherence to the code generation and review guidelines will help prevent
these recurring issues.

## Django-Specific Guidelines

### Environment Variable Management

1. Always store environment variables in the appropriate files:

   - `.env`
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

1. Use environment variables to manage sensitive information (e.g.,
   `os.environ`).

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

1. Write middleware to handle cross-cutting concerns (e.g., authentication,
   logging).

2. Ensure middleware adheres to Django’s lifecycle and compatibility.

### Application Testing

1. Write unit tests for views, models, and forms.

2. Use Django’s testing framework for integration tests.

3. Mock external dependencies to isolate test cases.

### Deployment

1. Use POSIX-compliant tools for deployment (e.g., `gunicorn`, `nginx`).

2. Ensure the application runs in a virtual environment.

3. Use environment variables for configuration in production.

### Template Structure Guidelines

#### Transaction Pipeline Template

```html
{% extends "layouts/dashboard_base.html" %} {% block title %}Transaction
Pipeline{% endblock title %} {% block dashboard_content %}
<h2>Transaction Data</h2>
<table>
  <tr>
    <th>ID</th>
    <th>User</th>
    <th>Status</th>
    <th>Timestamp</th>
  </tr>
  {% for transaction in transactions %}
  <tr>
    <td>{{ transaction.id }}</td>
    <td>{{ transaction.userId }}</td>
    <td>{{ transaction.status }}</td>
    <td>{{ transaction.timestamp }}</td>
  </tr>
  {% endfor %}
</table>
{% endblock dashboard_content %}
```

#### Data Processing Templates

```html
{% for transaction in enriched_transactions %}
<tr>
  <td>{{ transaction.id }}</td>
  <td>{{ transaction.user.name }}</td>
  <td>{{ transaction.status }}</td>
  <td>{{ transaction.timestamp }}</td>
</tr>
{% endfor %}
```

#### Pipeline Management Template

```html
{% extends "layouts/dashboard_base.html" %} {% block title %}System
Monitoring{% endblock title %} {% block dashboard_content %}
<h2>Pipeline Status</h2>
<p>Active Transactions: {{ active_transactions }}</p>
<p>Pending Retries: {{ pending_retries }}</p>
{% endblock dashboard_content %}
```

#### Error Management Templates

### 500 - Server Error Template

```html
{% extends "base.html" %} {% block title %}Server Error{% endblock title %} {%
block content %}
<h1>500 - Server Error</h1>
<p>Something went wrong. Our team is investigating.</p>
{% endblock content %}
```

### 403 - Access Denied Template

```html
{% extends "base.html" %} {% block title %}Access Denied{% endblock title %} {%
block content %}
<h1>403 - Forbidden</h1>
<p>You do not have permission to access this page.</p>
{% endblock content %}
```

#### Template Design Principles

1. **Modularity**

   - Use template inheritance with `{% extends %}` and `{% include %}`
   - Separate layouts, components, and partials
   - Create reusable blocks for common elements

2. **Data-Oriented Structure**

   - Focus on data presentation and workflow visualization
   - Use semantic HTML for data tables and forms
   - Implement proper ARIA labels and roles

3. **Pipeline Integration**

   - Create templates for each pipeline stage
   - Display workflow status and progress
   - Include monitoring and logging views

4. **Security Focus**

   - Implement proper CSRF protection
   - Display appropriate access control messages
   - Include security-related UI components

5. **Error Handling**
   - Create comprehensive error templates
   - Display user-friendly error messages
   - Include retry mechanism indicators

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
-- Create the obligations table with improved data types and constraints
CREATE TABLE Obligations (
    obligation__number VARCHAR(20) PRIMARY KEY,
    project__name VARCHAR(255) NOT NULL,
    primary__environmental__mechanism TEXT,
    procedure TEXT,
    environmental__aspect TEXT,
    obligation TEXT NOT NULL,
    accountability VARCHAR(255),
    responsibility VARCHAR(255),
    project_phase TEXT,
    action__due_date DATE,
    close__out__date DATE,
    status VARCHAR(50) CHECK (status IN ('not started', 'in progress', 'completed')),
    supporting__information TEXT,
    general__comments TEXT,
    compliance__comments TEXT,
    non_conformance__comments TEXT,
    evidence TEXT,
    person_email VARCHAR(255),  -- Added specific type for email
    recurring__obligation BOOLEAN DEFAULT FALSE,
    recurring__frequency VARCHAR(50),
    recurring__status VARCHAR(50),
    recurring__forcasted__date DATE,
    inspection BOOLEAN DEFAULT FALSE,
    inspection__frequency VARCHAR(50),
    site_or__desktop VARCHAR(50) CHECK (site_or__desktop IN ('Site', 'Desktop')),
    new__control__action_required BOOLEAN DEFAULT FALSE,
    obligation_type VARCHAR(50),
    gap__analysis TEXT,
    notes_for__gap__analysis TEXT,
    covered_in_which_inspection_checklist VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Added audit fields
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Add indexes for frequently queried fields
    INDEX idx_project_name (project__name),
    INDEX idx_status (status),
    INDEX idx_due_date (action__due_date),
    INDEX idx_phase (project_phase)
);

-- Trigger to update the updated_at timestamp
CREATE TRIGGER update_obligations_timestamp
    BEFORE UPDATE ON Obligations
    FOR EACH ROW
    SET NEW.updated_at = CURRENT_TIMESTAMP;
```

## User Journey

- Create a basic homepage template with welcome message, navigation links, and
  app info.

### Develop the Landing Page

- Create a basic homepage template with welcome message, navigation links, and
  information about the app.
- Add sections like social media links, testimonials, and FAQ.

### Create the Login Page

- Implement the login form with handling for both successful and unsuccessful
  logins.
- Set up password reset functionality.

### Develop the Dashboard

- Create a dashboard view displaying user activity, notifications, and quick
  links.
- Add a logout feature that redirects to the landing home page.
- Implement CRUD operations for user info updates, password changes, and
  profile pictures.

### Implement User Profile Management

- Create views for viewing and editing user profiles.
- Implement CRUD operations for updating user information, changing passwords,
  and uploading profile pictures.

### Set Up Admin Panel for User Management

- Enable Django’s admin interface to manage users, assign roles, and perform
  CRUD operations.

### Set Up Auditing for User Changes

- Implement logging for user actions (e.g., changes to profiles, user
  deletions).
- Use Django's built-in logging system.

### Create Dynamic Charts for Project Database Records

- Implement basic data visualizations for 14-day lookahead, overdue
  obligations, and obligations progress.
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
5. **Python**: Programming language for backend development.
6. **MatPlotLib**: Python plotting library.
7. **Pip**: Python package manager.
8. **Django-HTMX**: Python implementation of the library for AJAX interactions
   with HTMX to use in Django.
9. **Modern-Normalize**: CSS reset library.
10. **NVM**: Node Version Manager for managing Node.js versions.
11. **Node.js**: JavaScript runtime for frontend development.
12. **NPM**: Node Package Manager for frontend dependencies.
13. **Autopep8**: Python code formatter.
14. **Pylance**: Python language server for Visual Studio Code.
15. **Eslint**: JavaScript linter.
16. **Debugpy**: Python debugger for VS Code.
17. **Django-Hyperscript**: Python implementation to use hyperscript in Django.
18. **venv**: Python virtual environment tool.
19. **TailwindCSS**: Utility-first CSS framework.
20. **Django-Tailwind**: Python implementation of TailwindCSS for Django.

### Dependencies

1. Core Dependencies:

   - Django==4.2.20
   - matplotlib==3.9.4
   - django-htmx==1.22.0
   - django-hyperscript==1.0.2
   - django-tailwind==3.6.0

2. Development Tools:
   - djlint==1.36.4

### Frontend Dependencies

1. Node.js Environment:

   - Node.js 18.20.7 (exact version)
   - npm 10.8.2 (exact version)

2. Required Libraries:
   - tailwindcss==3.3.2

### NPM Configuration

1. Required Settings:
   - engine-strict=true
   - save-exact=true
   - audit=true
   - package-lock=true
   - resolution-mode=highest
   - fund=false

### Step-by-Step Instructions

1. **Set Up Environment**:

   - Install Python, SQLite3, and Podman.
   - Create a virtual environment using `python -m venv env`.

2. **Initialize Django Project**:

   - Run `django-admin startproject project_name`.
   - Set up the database connection in `settings.py` to use SQLite3.

3. **Create Database Schema**:

   - Use the Django ORM to define models based on the provided SQL schema for
     the obligations table.
   - Run `python manage.py makemigrations` to generate migrations.
   - Run `python manage.py migrate` to apply the schema to the SQLite3
     database.

4. **Develop the Landing Page**:

   - Create a new app using `python manage.py startapp landing`.
   - Add the app to `INSTALLED_APPS` in `settings.py`.
   - Define a `LandingPageView` class in `views.py` and create a corresponding
     template.
   - Use HTMX to add interactivity for sections like FAQs or testimonials.

5. **Create the Login Page**:

   - Use Django-allauth authentication system.
   - Create a `LoginView` and customize the template for user-friendly design.
   - Add password reset views and templates.

6. **Develop the Dashboard**:

   - Create a `DashboardView` in a new app (e.g., `dashboard`).
   - Fetch and display user-specific data using Django ORM.
   - Add logout functionality by linking to Django's `LogoutView`.

7. **Implement User Profile Management**:

   - Add a `UserProfile` model to store additional user information.
   - Create views and forms for profile editing, password changes, and profile
     picture uploads.

8. **Set Up the Admin Panel**:

   - Customize the Django admin interface for managing users and obligations.
   - Use `@admin.register` to register models with custom configurations.

9. **Set Up Auditing**:

   - Use Django’s logging framework to log user actions.
   - Add middleware or signal handlers to track changes and write logs.

10. **Create Dynamic Charts**:

    - Use Apache ECharts for visualizations in the dashboard.
    - Pass data to templates using Django context or AJAX calls with HTMX.

11. **Add Additional Features**:
    - Implement a help section using static pages.
    - Create account settings and notification preferences views.
    - Add feedback forms using Django’s forms framework.

### Technical Requirements

1. Python Version:

   - Python 3.9.21 (exact version)
   - Email: `agallo@enveng-group.com.au`

### Django Version Metadata

1. Django Version:

   - Django 4.2.20 (exact version)
   - Ensure compatibility with Django 5.1.x features
   - Email: [agallo@enveng-group.com.au](mailto:agallo@enveng-group.com.au)

### Author Metadata

1. Author Information:

   - Author: Adrian Gallo
   - Email: [agallo@enveng-group.com.au](mailto:agallo@enveng-group.com.au)
   - License: AGPL-3.0
