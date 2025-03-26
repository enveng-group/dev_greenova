# Greenova Project Technical Context

## Core Principles

- **Simplicity First**: Prioritize plain text and HTML-first approaches by
  design
- **Technology Priority**: Use technologies in this specific order of
  preference:
  1. Plain text / HTML (foundational)
  2. Protobuf3 (data formats)
  3. Classless-CSS (styling)
  4. hyperscript (simple interactions)
  5. htmx (more complex AJAX)
  6. SASS/PostCSS (advanced styling when needed)
  7. TypeScript (only when absolutely necessary)
  8. AssemblyScript (for WASM, last resort only)
- **Data-Oriented Programming**: Focus on immutable data structures and
  functional transformations
- **5S Methodology**: Apply Sort (整理), Set in order (整頓), Shine (清掃),
  Standardize (清潔), and Sustain (躾)
- **Standards Compliance**: Adhere to strict industry coding standards,
  including POSIX/ISO where applicable
- **Value Hierarchy**: Prioritize stability, simplicity, minimalism, and
  security over performance and speed

## Project Domain

Greenova is a Django web application for environmental management, focusing on
tracking environmental obligations and compliance requirements.

## Technical Stack

We use Python 3.9.21 with Django 4.1.13 for backend development.

Our frontend uses Classless-PicoCSS as the primary CSS framework. Tailwind CSS should
only be used for specialized UI components when PicoCSS cannot handle the
requirements, and only after all simpler solutions have been exhausted.

We implement frontend interactivity with django-hyperscript for simple
interactions and django-htmx for more complex AJAX functionality. Custom
TypeScript and AssemblyScript (for WASM) is only used as a last resort when no
simpler solution exists.

We use matplotlib for server-side data visualization, adhering to data-oriented
principles.

Our database is SQLite3 in development, with careful attention to data
integrity and immutability.

We deploy using Docker containers with minimal, secure configurations.

## Development Practices

We follow an HTML-first approach with progressive enhancement, starting with
semantic, accessible, and minimal HTML.

We prioritize WCAG 2.1 AA standards for accessibility in all interfaces.

We use test-driven development with Django's testing framework. All models,
forms, and views should have corresponding unit tests to ensure stability.

We organize code in a modular Django architecture with specialized apps for
different functional areas following the 5S principle of organization.

We use class-based views with minimal mixins for code reuse in Django.

We implement proper model relationships and constraints in our database design,
focusing on data integrity and immutability.

We handle authentication using django-allauth with multi-factor authentication
support for security.

## Data Structure

Our primary data model is the Obligation model which tracks environmental
compliance requirements. Obligations are related to Projects, Mechanisms, and
Procedures.

Users are assigned Responsibilities related to Obligations.

We strictly follow data-oriented programming principles with immutable data
structures and functional transformations. Mutation should be avoided wherever
possible.

## Version Control and Quality

We use git with pre-commit hooks.

We enforce code quality with pylint, pylint-django, eslint, djlint, and
markdownlint.

We format code with autopep8, prettier, and isort.

We use mypy with django-stubs for strict type checking Python code.

## Dependencies

We maintain exact versions of dependencies:

- Python 3.9.21
- Django 4.1.13
- Node.js 18.20.7
- NPM 10.8.2
- @picocss/pico 2.0.6
- htmx.org 1.9.12
- hyperscript.org 0.9.14
