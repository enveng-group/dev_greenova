# Pull Request Template

## Title

`release(v0.0.5): comprehensive platform enhancements and new features`

## Description

### Purpose

Pre-release v0.0.5 integrating multiple feature branches and improvements
across the Greenova platform. This release enhances development infrastructure,
user experience, testing capabilities, and adds new functional modules for
company management and user profiles.

### Changes

#### Development Infrastructure

- Updated development tooling with enhanced pre-commit hooks and custom pylint
  extensions.
- Configured mypy with django-stubs for better type checking.
- Standardized editor configuration and VSCode settings.
- Improved devcontainer configuration with Snyk CLI and Git features.
- Integrated Sentry for error tracking.
- Added direnv support for environment variable management.
- Configured Prettier for consistent code formatting.
- Migrated to dotenv-vault for environment management.

#### UI/UX Improvements

- Enhanced landing page with mission statement and key features sections.
- Implemented theme switching functionality with WCAG 2.1 AA compliance.
- Refined dashboard interface, navigation, and component organization.
- Added responsive layouts and improved semantic HTML structure.
- Optimized chart generation with centralized logic in `figures.py`.
- Reorganized CSS directory structure for better organization.
- Enhanced breadcrumb component with better styling and accessibility.

#### New Features

- **Company Management Module**
  - Company models, views, and templates.
  - Document management capabilities.
  - Member role management.
  - Navigation integration.
  - CSS styling for company components.
- **User Profile Functionality**
  - Complete user profile management.
  - Password change capability.
  - Admin interfaces for user management.
- **Chatbot Development**
  - Implemented chatbot conversation management.
  - Added chatbot message styles and variables.
  - Chatbot serialization and protocol buffer support.

#### Testing and Quality

- Integrated pytest framework with comprehensive test coverage across all apps.
- Added new test files for authentication, chatbot, company, core, and other
  modules.
- Refactored code structure to improve testability.
- Implemented ESLint for JavaScript.
- Added djlint for Django HTML templates.
- Configured autopep8 for Python formatting.

#### Documentation

- Restructured `docs/resources` with logical subdirectories.
- Added commit message templates, code review templates, and GitHub issue
  templates.
- Updated environment configuration documentation and technical guides.
- Added GitHub CLI usage instructions.
- Included changelog references.
- Enhanced front-end interactivity documentation.
- Added comprehensive Makefile comments.

#### Dependencies

- Updated packages for compatibility with Python 3.9.21 and Django 4.1.13.
- Downgraded matplotlib version for compatibility.
- Revised environment variable configurations in `.env.vault`.
- Included pre-commit dependency in `requirements.txt`.

### Related Issues

- Closes #33, #41

### Testing Performed

- Comprehensive test suite execution with pytest.
- Manual testing of new company management features.
- User profile functionality verification.
- Chatbot interaction testing.
- Theme switching and accessibility compliance validation.
- Cross-browser compatibility testing.

### Deployment Notes

- Contains multiple database migrations.
- Requires updated environment variables via `.env.vault`.
- Updated dependency requirements need to be installed.
- Sentry integration requires configuration of Sentry DSN.

### Contributors

- [agallo](https://github.com/enveng-group)
- [JaredStanbrook](https://github.com/JaredStanbrook)
- [cameronsims](https://github.com/cameronsims)
- [Channing88](https://github.com/Channing88)
- [muhammadhaseebahmad](https://github.com/mhahmad0)
