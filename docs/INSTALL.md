<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Installation Guide (Updated for pip-tools and constraints)](#installation-guide-updated-for-pip-tools-and-constraints)
  - [System Requirements](#system-requirements)
  - [Development Setup](#development-setup)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Installation Guide (Updated for pip-tools and constraints)

## System Requirements

- Python 3.12.10
- SQLite3
- pip package manager

## Development Setup

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

4. Install dependencies with pip-sync:

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

> **Note:** All dependencies are managed with pip-tools and constraints.txt for
> reproducibility. See requirements/README.md for details.
