# Greenova Project Technical Context

## Project Domain

Greenova is a Django web application for environmental management, focusing on
tracking environmental obligations and compliance requirements.

## Technical Stack

We use Python 3.9.21 with Django 4.1.13 for backend development.

Our frontend uses PicoCSS as the primary CSS framework. Only use Tailwind CSS

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

We follow data-oriented programming principles with immutable data structures
and functional transformations.

## Version Control and Quality

We use git with pre-commit hooks.

We enforce code quality with pylint, pylint-django, eslint, djlint, and
markdownlint.

We format code with autopep8, prettier, and isort.

We use mypy with django-stubs for type checking Python code.

## Dependencies

We maintain compatible versions of dependencies:

- Python 3.9.21
- Django 4.1.13
- Node.js 18.20.7
- NPM 10.8.2
- @picocss/pico 2.0.6
- htmx.org 1.9.12
- hyperscript.org 0.9.14
