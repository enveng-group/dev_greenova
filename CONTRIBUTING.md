# Contributing to Greenova

Thank you for your interest in contributing to Greenova! This document provides
guidelines and workflows to help make the contribution process straightforward
and effective.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
  - [Development Environment Setup](#development-environment-setup)
- [How to Contribute](#how-to-contribute)
  - [Reporting Issues](#reporting-issues)
  - [Feature Requests](#feature-requests)
  - [Documentation Updates](#documentation-updates)
  - [Code Contributions](#code-contributions)
- [Development Workflow](#development-workflow)
  - [Fork-Based Contribution](#fork-based-contribution)
  - [Git Workflow for Direct Contributors](#git-workflow-for-direct-contributors)
  - [Branch Strategy](#branch-strategy)
  - [Commit Message Guidelines](#commit-message-guidelines)
- [Pull Request Process](#pull-request-process)
  - [Pull Request Checklist](#pull-request-checklist)
  - [Code Review Process](#code-review-process)
- [Coding Standards](#coding-standards)
  - [Python Code Style](#python-code-style)
  - [HTML/CSS Guidelines](#htmlcss-guidelines)
  - [JavaScript Standards](#javascript-standards)
  - [Testing Requirements](#testing-requirements)
  - [Documentation Requirements](#documentation-requirements)
- [Project Structure](#project-structure)
- [Community](#community)
  - [Getting Help](#getting-help)

## Code of Conduct

Our project adheres to a code of conduct that all contributors are expected to
follow. By participating, you are expected to uphold this code. Please report
unacceptable behavior to the project maintainers.

We value respect, inclusivity, and a collaborative environment where everyone
feels welcome to contribute.

## Getting Started

### Development Environment Setup

1. **Prerequisites**:

   - Python 3.9.21
   - Node.js 18.20.7
   - NPM 10.8.2
   - Git

2. **Clone the repository** (if you're a direct contributor) or fork it first
   (recommended for external contributors):

   ```bash
   git clone https://github.com/enssol/greenova.git
   cd greenova
   ```

3. **Set up a virtual environment**:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

4. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   npm install
   ```

5. **Apply database migrations**:

   ```bash
   python manage.py migrate
   ```

6. **Create a superuser** (for admin access):

   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**:

   ```bash
   python manage.py runserver
   ```

The application will be available at
[http://localhost:8000](http://localhost:8000).

## How to Contribute

### Reporting Issues

If you find a bug or have a suggestion for improvement:

1. Check if the issue already exists in the
   [GitHub Issues](https://github.com/enssol/greenova/issues)
2. If not, [create a new issue](https://github.com/enssol/greenova/issues/new)
   with:
   - A clear, descriptive title
   - Detailed steps to reproduce (for bugs)
   - Expected and actual behavior
   - Screenshots if applicable
   - Your environment details (OS, browser, etc.)

### Feature Requests

For feature requests:

1. Describe the feature in detail
2. Explain the use case and benefits
3. Indicate if you're willing to contribute the feature yourself

### Documentation Updates

Documentation improvements are always welcome:

- Fix typos or clarify existing content
- Add missing information
- Update documentation to reflect current functionality

### Code Contributions

For code contributions, please follow our
[Development Workflow](#development-workflow).

## Development Workflow

We use a fork-based workflow for external contributors and a feature branch
workflow for direct contributors.

### Fork-Based Contribution

For external contributors:

1. **Fork the repository** on GitHub
2. **Clone your fork**:

   ```bash
   git clone https://github.com/YOUR-USERNAME/greenova.git
   cd greenova
   ```

3. **Add upstream remote**:

   ```bash
   git remote add upstream https://github.com/enssol/greenova.git
   ```

4. **Keep your fork updated**:

   ```bash
   git fetch upstream
   git checkout main
   git reset --hard upstream/main
   git push origin main
   ```

5. **Create a feature branch**:

   ```bash
   git checkout -b feature-name
   ```

6. **Make your changes** and commit with
   [proper commit messages](#commit-message-guidelines)

7. **Keep your branch updated** during development:

   ```bash
   git fetch upstream
   git rebase upstream/main
   # Resolve any conflicts
   ```

8. **Push your changes** to your fork:

   ```bash
   git push origin feature-name
   ```

9. **Create a pull request**:
   - Ensure your branch is up to date with upstream
   - Submit the pull request through GitHub

### Git Workflow for Direct Contributors

For direct contributors:

1. **Update your main branch**:

   ```bash
   git checkout main
   git pull origin main
   ```

2. **Create a feature branch**:

   ```bash
   git checkout -b feature-name
   ```

3. **Make your changes** and commit with
   [proper commit messages](#commit-message-guidelines)

4. **Squash and merge your feature branch**:

   ```bash
   git checkout main
   git merge --squash feature-name
   git commit -m "feat: squashed commit message"
   ```

5. **Push changes to main**:

   ```bash
   git push origin main
   ```

6. **Delete the feature branch**:

   ```bash
   git branch -D feature-name
   git push origin --delete feature-name
   ```

### Branch Strategy

- Use `main` for production-ready code
- Use `pre-release` branches for upcoming releases
- Use feature branches for new features or bug fixes

### Commit Message Guidelines

Follow the [Conventional Commits](https://www.conventionalcommits.org/)
standard:

- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Example:

```bash
git commit -m "feat: add user authentication"
```

## Pull Request Process

### Pull Request Checklist

Before submitting a pull request:

1. Ensure your branch is up to date with `main`
2. Run tests and ensure they pass
3. Follow coding standards
4. Provide a clear description of the changes
5. Reference related issues (if any)

### Code Review Process

- Pull requests will be reviewed by maintainers
- Address feedback promptly
- Make additional commits to your branch as needed

## Coding Standards

### Python Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use type hints where applicable
- Write docstrings for all functions and classes

### HTML/CSS Guidelines

- Follow [W3C standards](https://www.w3.org/)
- Use semantic HTML
- Keep CSS modular and reusable

### JavaScript Standards

- Follow [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- Use ES6+ features
- Write unit tests for all functions

### Testing Requirements

- Write tests for new features and bug fixes
- Use pytest for Python tests
- Use Jest for JavaScript tests

### Documentation Requirements

- Update documentation for new features
- Ensure examples are clear and accurate

## Project Structure

- `src/`: Source code
- `tests/`: Test cases
- `docs/`: Documentation
- `assets/`: Static files (images, CSS, JS)

## Community

### Getting Help

If you need help:

- Check the
  [GitHub Discussions](https://github.com/enssol/greenova/discussions)
- Reach out to maintainers via email
- Join our Slack channel (link available in the repository)

Thank you for contributing to Greenova!
