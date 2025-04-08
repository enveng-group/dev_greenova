<!-- markdownlint-configure-file { "MD024": { "allow_different_nesting": true } } -->

# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased] - Upcoming Release

### Added

- None

### Changed

- None

### Deprecated

- None

### Removed

- None

### Fixed

### Security

- None

[Unreleased]: https://github.com/username/greenova/compare/v0.0.5...HEAD
[v0.0.5]: https://github.com/username/greenova/compare/v0.0.4...v0.0.5
[v0.0.4]: https://github.com/username/greenova/compare/v0.0.3...v0.0.4
[v0.0.3]: https://github.com/username/greenova/compare/v0.0.2...v0.0.3
[v0.0.2]: https://github.com/username/greenova/compare/v0.0.1...v0.0.2
[v0.0.1]: https://github.com/username/greenova/releases/tag/v0.0.1

- None

## [v0.0.5] - Pre-release

### Added

- **Development Infrastructure**

  - Updated development tooling with enhanced pre-commit hooks and custom
    pylint extensions.
  - Configured mypy with django-stubs for better type checking.
  - Standardized editor configuration and VSCode settings.
  - Improved devcontainer configuration with Snyk CLI and Git features.
  - Integrated Sentry for error tracking.
  - Added direnv support for environment variable management.
  - Configured Prettier for consistent code formatting.
  - Migrated to dotenv-vault for environment management.

- **UI/UX Improvements**

  - Enhanced landing page with mission statement and key features sections.
  - Implemented theme switching functionality with WCAG 2.1 AA compliance.
  - Refined dashboard interface, navigation, and component organization.
  - Added responsive layouts and improved semantic HTML structure.
  - Optimized chart generation with centralized logic in `figures.py`.
  - Reorganized CSS directory structure for better organization.
  - Enhanced breadcrumb component with better styling and accessibility.

- **New Features**
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

### Changed

- Refactored code structure to improve testability.
- Enhanced front-end interactivity documentation.
- Updated environment configuration documentation and technical guides.
- Restructured `docs/resources` with logical subdirectories.
- Added commit message templates, code review templates, and GitHub issue
  templates.
- Updated packages for compatibility with Python 3.9.21 and Django 4.1.13.
- Downgraded matplotlib version for compatibility.
- Revised environment variable configurations in `.env.vault`.
- Included pre-commit dependency in `requirements.txt`.

### Fixed

- Comprehensive test suite execution with pytest.
- Manual testing of new company management features.
- User profile functionality verification.
- Chatbot interaction testing.
- Theme switching and accessibility compliance validation.
- Cross-browser compatibility testing.

### Security

- Integrated Sentry for error tracking.

## [v0.0.4] - Pre-release

### Added

- **Company Management Module**
  - Company models, views and templates
  - Document management capabilities
  - Member role management
  - Navigation integration
  - CSS styling for company components
- **User Profile Functionality**
  - Complete user profile management
  - Password change capability
  - Admin interfaces for user management
- **Chatbot Development**
  - Implement chatbot conversation management
  - Add chatbot message styles and variables
  - Chatbot serialization and protocol buffer support
- Implement theme switching functionality with WCAG 2.1 AA compliance
- Add responsive layouts and improve semantic HTML structure
- Integrate pytest framework with comprehensive test coverage across all apps
- Add new test files for authentication, chatbot, company, core, and other
  modules
- Integrate Sentry for error tracking
- Add direnv support for environment variable management

### Changed

- Enhance landing page with mission statement and key features sections
- Refine dashboard interface, navigation, and component organization
- Optimize chart generation with centralized logic in figures.py
- Reorganize CSS directory structure for better organization
- Enhance breadcrumb component with better styling and accessibility
- Update dev tooling with enhanced pre-commit hooks and custom pylint
  extensions
- Configure mypy with django-stubs for better type checking
- Standardize editor configuration and VSCode settings
- Improve devcontainer configuration with Snyk CLI and Git features
- Configure Prettier for consistent code formatting
- Migrate to dotenv-vault for environment management
- Update packages for compatibility with Python 3.9.21 and Django 4.1.13
- Downgrade matplotlib version for compatibility
- Revise environment variable configurations in .env.vault
- Include pre-commit dependency in requirements.txt
- Restructure docs/resources with logical subdirectories
- Update environment configuration documentation and technical guides

### Deprecated

- None

### Removed

- None

### Fixed

- Refactor code structure to improve testability
- Add comprehensive Makefile comments

### Security

- Implement ESLint for JavaScript
- Add djlint for Django HTML templates
- Configure autopep8 for Python formatting

## [v0.0.3] - Pre-release

### Added

- Implemented light/dark mode theming with CSS variables
- Added dedicated navigation.css for consistent cross-application navigation
- Replaced Django auth with django-allauth for enhanced user management
- Added comprehensive registration, login, and account management flows
- Added user login toggle feature with persistent/session-based authentication
  options
- Added procedures app with visualization components and chart templates
- Added responsibility module with distribution charts and models
- Added django-debug-toolbar for development troubleshooting
- Added comprehensive git repository management guidelines
- Added new project documentation for UI design, data visualization, and
  frontend architecture
- Implemented HTMX and Hyperscript integration for progressive enhancement

### Changed

- Refined UI components (forms, buttons, cards, lists) for improved usability
- Enhanced typography system with standardized sizing and spacing
- Optimized chart styling and scaling for better data visualization
- Improved color scheme with accessibility considerations
- Revamped authentication flow with updated templates
- Enhanced dashboard layout with improved information hierarchy
- Refined landing page with better user onboarding elements
- Improved project selector component with dynamic filtering
- Optimized obligation view templates with clearer data presentation
- Enhanced devcontainer configuration for consistent development environment
- Created constraints.txt for precise dependency pinning and compatibility
- Updated package.json with current frontend dependencies
- Refined Makefile targets for streamlined development workflows
- Upgraded .pyrightconfig.json for improved type checking
- Converted documentation files to Markdown format
- Set light-mode as default theme
- Reorganized and optimized CSS structure

### Deprecated

- None

### Removed

- Removed deprecated CSV files (dirty.csv, clean_output_with_nulls.csv)
- Temporarily removed Ubuntu font

### Fixed

- Fixed theme auto-discoloration by enforcing CSS variables with !important
- Fixed issues with duplicate component rendering
- Fixed missing obligation lists and rendering issues
- Fixed project structure and file tracking issues

### Security

- Set minimum password length to 9 characters
- Prepared for future social auth integrations

## [v0.0.2] - Pre-release

### Added

- Enhanced obligations model with improved field definitions and constraints
- Updated import tool for obligations data
- Refined admin interface for better obligations management

### Changed

- Updated Makefile with new development commands
- Improved obligations data handling and validation

### Deprecated

- None

### Removed

- None

### Fixed

- None

### Security

- None

## [v0.0.1] - Pre-release

### Added

- Updated devcontainer configuration for improved performance and consistency.
- Added new VS Code extensions and settings for Python, JavaScript, and HTML
  development.
- Configured .env files for better environment variable management.
- Upgraded Python version to 3.9.
- Updated Django to version 5.1.6.
- Added new dependencies such as matplotlib for data visualization.
- Implemented djlint for linting and formatting Django templates.
- Configured autopep8 for Python code formatting.
- Added ESLint configuration for JavaScript linting.
- Created a Makefile with common commands for development and deployment.
- Added scripts for database migrations, static file collection, and server
  start.
- Refined project structure and updated .gitignore to exclude unnecessary
  files.
- Removed deprecated and unused files.
- Updated README.md with new setup instructions.
- Added CHANGELOG, CONTRIBUTING, SECURITY, and SUPPORT documentation.
- Configured GitHub Actions for automated testing and deployment.

### Changed

- None

### Deprecated

- None

### Removed

- None

### Fixed

- None

### Security

- None
