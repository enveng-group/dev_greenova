# Greenova

[![Python 3.9.21](https://img.shields.io/badge/python-3.9.21-blue.svg)](https://www.python.org/downloads/release/python-3921/)
[![Django 4.1.13](https://img.shields.io/badge/django-4.1.13-green.svg)](https://www.djangoproject.com/)
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

### Backend

- Python 3.9.21
- Django 4.1.13
- SQLite3 (development)
- Matplotlib 3.10.0
- Django-HTMX 1.22.0
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

- Python 3.9.21
- Node.js 18.20.7
- NPM 10.8.2

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/enssol/greenova.git
   cd greenova
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Install Node.js dependencies:

   ```bash
   npm install
   ```

5. Apply migrations:

   ```bash
   python manage.py migrate
   ```

6. Create a superuser:

   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:

   ```bash
   python manage.py runserver
   ```

## 🔧 Usage

Access the application at [http://localhost:8000](http://localhost:8000) after
starting the development server.

### Key workflows

1. Log in using the credentials created during setup
2. Create projects and define environmental mechanisms
3. Add obligations related to your projects
4. Assign responsibilities to users
5. Monitor compliance status

## 🤝 Contributing

We welcome contributions to Greenova! Please check our contributing guidelines
in the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## 📄 License

This project is licensed under the GNU Affero General Public License v3.0 - see
the [LICENSE](LICENSE) file for details.

## 📊 Project Status

Greenova is under active development. Check our [roadmap](docs/ROADMAP.md) for
upcoming features and improvements.
