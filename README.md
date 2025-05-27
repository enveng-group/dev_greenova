# Greenova

[![Python 3.12.9](https://img.shields.io/badge/python-3.12.9-blue.svg)](https://www.python.org/downloads/release/python-3921/)
[![Django 5.2](https://img.shields.io/badge/django-5.2-green.svg)](https://www.djangoproject.com/)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

## 📋 Overview

Greenova is a Django web application designed for environmental management,
focusing on tracking environmental obligations and compliance requirements.
Built with accessibility and simplicity in mind, it helps organizations manage
their environmental responsibilities efficiently.

## 🚀 Features

- Environmental obligation tracking
- Compliance requirement management
- Project-based organization
- Mechanism and procedure documentation
- User responsibility assignment
- Accessible, HTML-first interface

## 🛠️ Technology Stack

Greenova is a Django web application that prioritizes semantic HTML structure,
progressive enhancement, and accessibility. The project follows data-oriented
programming principles and provides a modular framework for building robust web
applications.

- Django-Hyperscript 1.0.2
- Django-Tailwind 3.6.0
- Django-Allauth 65.4.1

### Frontend

- HTML5
- PicoCSS (classless framework)
- Django-Tailwind (for utility classes)
- Modern-Normalize

### DevOps

- Docker
- GitHub CI/CD
- venv (virtual environment)

## 🏛️ Architecture

The application follows a modular design with clear separation of concerns:

1. **Data Definition Layer**: Immutable data structures with validation
2. **Data Processing Layer**: Functional transformations using map, filter, and
   reduce
3. **Data Flow Layer**: Pipelines for managing workflow
4. **Exception Handling Layer**: Business rule and system exception management
5. **Data Storage Layer**: Immutable data storage with optimized queries
6. **Automation Layer**: Task execution and monitoring
7. **Security Layer**: Role-based access control and data encryption

## 📥 Installation

### Prerequisites

- Python 3.12.9
- Node.js 20.19.1
- NPM 11.3.0

### Setup

1. Clone the repository:

   ```fish
   git clone https://github.com/enssol/greenova.git
   cd greenova
   ```

2. Create and activate a virtual environment:

   ```fish
   python3 -m venv .venv
   source .venv/bin/activate.fish
   ```

3. Install pip-tools and compile requirements:

   ```fish
   pip install --upgrade pip pip-tools
   pip-compile requirements/requirements.in
   pip-compile requirements/requirements-dev.in
   pip-compile requirements/requirements-prod.in
   pip-compile --all-build-deps --all-extras --output-file=requirements/constraints.txt --strip-extras requirements/requirements.in
   ```

4. Install Python dependencies with pip-sync:

   ```fish
   pip-sync requirements/requirements.txt requirements/requirements-dev.txt -c requirements/constraints.txt
   ```

5. Install Node.js dependencies:

   ```fish
   npm install
   ```

6. Apply migrations:

   ```fish
   python manage.py migrate
   ```

7. Create a superuser:

   ```bash
   python manage.py createsuperuser
   ```

8. Run the development server:

   ```bash
   python manage.py runserver
   ```

> **Note:** All dependencies are managed with pip-tools and constraints.txt for
> reproducibility. See requirements/README.md for details.

## Dependency Management

The Greenova project uses a structured approach to manage Python dependencies,
ensuring consistency across development, testing, and production environments.
The dependencies are organized as follows:

### Requirements Directory

- **`requirements/requirements.in`**: Contains essential runtime dependencies
  required for the application to function.
- **`requirements/requirements-dev.in`**: References `requirements.in` and
  includes additional dependencies for development, such as testing and linting
  tools.
- **`requirements/requirements-prod.in`**: References `requirements.in` and
  includes production-specific dependencies, such as WSGI servers.
- **`requirements/constraints.txt`**: Pins versions for all dependencies (both
  direct and indirect) to ensure reproducible builds.

### Usage

- **Development Environment**:

  - Install dependencies using:

    ```bash
    pip-sync requirements/requirements.txt requirements/requirements-dev.txt -c requirements/constraints.txt
    ```

- **Production Environment**:

  - Install dependencies using:

    ```bash
    pip-sync requirements/requirements.txt requirements/requirements-prod.txt -c requirements/constraints.txt
    ```

### Devcontainer Setup

The `.devcontainer` configuration automatically installs the development
dependencies (`requirements/requirements-dev.in`) when the container is built
or started. This ensures a consistent development environment.

### Setup.py

The `setup.py` file includes only the minimal core dependencies required for
runtime, with flexible version specifications. Additional development
dependencies are specified under `extras_require`.

### Benefits

- **No Duplication**: Dependencies are defined in a single location, avoiding
  inconsistencies.
- **Reproducibility**: Pinned versions in `constraints.txt` ensure consistent
  builds across environments.
- **Modularity**: Separate files for runtime, development, and production
  dependencies make it easy to manage and update.

Refer to the `requirements/` directory for detailed dependency specifications.

## Manual Installation of Microsoft Python Type Stubs

To enable type checking for certain libraries, you need to manually install the
`microsoft-python-type-stubs` package. This package is not available on PyPI
and must be installed directly from GitHub:

```bash
pip install git+https://github.com/microsoft/python-type-stubs.git
```

Ensure this is done in your development environment before running `mypy` or
other type-checking tools.

## Environment Variables

Greenova requires a `.env` file to store sensitive configuration values. Below
are the required and optional environment variables:

### Required Variables

- `DJANGO_SECRET_KEY`: The secret key for Django. Must be set to a secure
  value.
- `DJANGO_DEBUG`: Set to `True` for development or `False` for production.
- `DJANGO_ALLOWED_HOSTS`: A comma-separated list of allowed hostnames (e.g.,
  `localhost,127.0.0.1`).

### Optional Variables

- `GITHUB_CLIENT_ID`: GitHub OAuth client ID for social authentication.
- `GITHUB_CLIENT_SECRET`: GitHub OAuth client secret for social authentication.

### Creating the `.env` File

1. Create a `.env` file in the project root:

   ```bash
   touch .env
   ```

2. Populate the file with the required variables:

   ```env
   DJANGO_SECRET_KEY="your-secure-secret-key"
   DJANGO_DEBUG=True
   DJANGO_ALLOWED_HOSTS="localhost,127.0.0.1"
   ```

3. Add any optional variables as needed.

Ensure the `.env` file is not committed to version control by verifying it is
listed in `.gitignore`.

## 🔧 Usage

Access the application at [http://localhost:8000](http://localhost:8000) after
starting the development server.

### Key workflows

1. Log in using the credentials created during setup
2. Create projects and define environmental mechanisms
3. Add obligations related to your projects
4. Assign responsibilities to users
5. Monitor compliance status
6. CRUD user profiles and company information 7 Drill down into mechanisms,
   then into procedures, then into obligations for detailed information.
   - Perform CRUD operations on obligations.
7. When hovering over the overdue obligations card, a tooltip will display a
   list of overdue obligations.
   - Each overdue obligation will be listed and clickable, linking to its
     detail page.
   - You can edit individual obligation records from their detail pages.
   - Full CRUD operations are supported for overdue obligations.

## 🤝 Contributing

We welcome contributions to Greenova! Please check our contributing guidelines
in the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## 📄 License

This project is licensed under the GNU Affero General Public License v3.0 - see
the [LICENSE](LICENSE) file for details.

## 📊 Project Status

Greenova is under active development. Check our [roadmap](docs/ROADMAP.md) for
upcoming features and improvements.
