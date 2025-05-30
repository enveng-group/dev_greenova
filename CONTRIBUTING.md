<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Contributing to Greenova](#contributing-to-greenova)
  - [Table of Contents](#table-of-contents)
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
    - [Merge, Release, and Tagging Process](#merge-release-and-tagging-process)
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
  - [Secret Scanning and Gitleaks Workflow](#secret-scanning-and-gitleaks-workflow)
    - [How Gitleaks Works](#how-gitleaks-works)
    - [Workflow for Contributors](#workflow-for-contributors)
    - [Example: Redacting Secrets Automatically](#example-redacting-secrets-automatically)
    - [Configuration](#configuration)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

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
  - [Merge, Release, and Tagging Process](#merge-release-and-tagging-process)
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

   - Python 3.12.10
   - Node.js 21.7.3
   - NPM 10.9.1
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
- Use `pre-release` branches for upcoming releases (e.g.,
  `integration/[version]`)
- Use feature branches for new features or bug fixes

---

### Merge, Release, and Tagging Process

For each new release, follow a structured merge and release process. Always
consult the latest, detailed instructions in
`docs/resources/git/merge-instructions.txt` for up-to-date, release-specific
steps and best practices. The following is a generic summary:

1. **Repository Health Check**: Ensure your working directory is clean and up
   to date. Run repository health and optimization steps as described in the
   merge instructions.

2. **Changelog Preparation**: Update `CHANGELOG.md` to summarize all changes
   between `[previous release]` and `[current release]`.

3. **Branching**: Create or update an integration branch (e.g.,
   `integration/[version]`) from the latest staging or pre-release branch.

4. **Merging**: Merge feature branches and pull requests into the integration
   branch in a safe, logical order. Resolve conflicts according to project
   standards. Use placeholders for PR numbers and branch names (e.g.,
   `feature/[feature-name]`).

5. **Testing**: After each merge, run the full test suite and code quality
   checks. See the Testing Requirements section.

6. **Final Merge**: Merge the integration branch into `staging`, then into
   `main` (or the production branch). Resolve any remaining conflicts.

7. **Tagging and Release**: Tag the new release as `[version]` (e.g.,
   `v[version]`). Push the tag to the remote repository. Draft a new release in
   GitHub Releases, using the new tag and including release notes.

8. **Post-Release Maintenance**: Clean up merged branches, optimize the
   repository, and verify database integrity.

**Note:**

- Replace `[version]` with the current release version (e.g., `v1.2.3`).
- Replace `[previous release]` with the last release tag (e.g., `v1.2.2`).
- Always follow the detailed, up-to-date process in
  `docs/resources/git/merge-instructions.txt` for each release.

---

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

## Secret Scanning and Gitleaks Workflow

Greenova uses [Gitleaks](https://github.com/gitleaks/gitleaks) to detect and prevent accidental commits of secrets (API keys, passwords, tokens, etc.).

### How Gitleaks Works

- Gitleaks runs automatically as a pre-commit hook.
- It scans for secrets using a custom configuration in `.gitleaks.toml` and ignores known fingerprints in `.gitleaksignore`.
- Reports are generated in SARIF format as `gitleaks-report.json`.
- If secrets are detected, the commit will be blocked. You must remove or redact the secrets before committing.

### Workflow for Contributors

1. **Before committing:**
   - Run `pre-commit run gitleaks --all-files` to scan for secrets.
   - If secrets are found, review `gitleaks-report.json` and remove/redact any secrets.
   - If a finding is a false positive, add its fingerprint to `.gitleaksignore`.
2. **Baseline:**
   - If you need to update the baseline, run Gitleaks with `--report-path gitleaks-report.json` and use the report as a baseline for future scans.
3. **Redaction/Removal:**
   - Use the provided script in `scripts/gitleaks.py` or manually remove secrets if detected.

### Example: Redacting Secrets Automatically

A sample script (`scripts/gitleaks.py`) can be used to check for secrets in the report and block the commit if any are found:

```python
import sys
import json

with open("gitleaks-report.json", encoding="utf-8") as f:
    data = json.load(f)

if data:
    print("\n[ERROR] Gitleaks detected secrets! Please remove or redact them before committing.\n")
    sys.exit(1)
```

Add this script as a post-Gitleaks hook if you want to enforce blocking on secret detection.

### Configuration

- `.gitleaks.toml`: Custom rules and allowlists for the project.
- `.gitleaksignore`: Ignore specific fingerprints (one per line).

For more details, see the [Gitleaks documentation](https://github.com/gitleaks/gitleaks).
