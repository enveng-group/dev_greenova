# Pull Request Template

## Title

`release(v0.0.4): comprehensive platform enhancements and new features`

## Description

### Purpose

Pre-release v0.0.4 integrating multiple feature branches and improvements across the Greenova platform. This release enhances development infrastructure, user experience, testing capabilities, and adds new functional modules for company management and user profiles.

### Changes

#### Development Infrastructure

- Update dev tooling with enhanced pre-commit hooks and custom pylint extensions
- Configure mypy with django-stubs for better type checking
- Standardize editor configuration and VSCode settings
- Improve devcontainer configuration with Snyk CLI and Git features
- Integrate Sentry for error tracking
- Add direnv support for environment variable management
- Configure Prettier for consistent code formatting
- Migrate to dotenv-vault for environment management

#### UI/UX Improvements

- Enhance landing page with mission statement and key features sections
- Implement theme switching functionality with WCAG 2.1 AA compliance
- Refine dashboard interface, navigation, and component organization
- Add responsive layouts and improve semantic HTML structure
- Optimize chart generation with centralized logic in figures.py
- Reorganize CSS directory structure for better organization
- Enhance breadcrumb component with better styling and accessibility

#### New Features

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

#### Testing and Quality

- Integrate pytest framework with comprehensive test coverage across all apps
- Add new test files for authentication, chatbot, company, core, and other modules
- Refactor code structure to improve testability
- Implement ESLint for JavaScript
- Add djlint for Django HTML templates
- Configure autopep8 for Python formatting

#### Documentation

- Restructure docs/resources with logical subdirectories
- Add commit message templates, code review templates, and GitHub issue templates
- Update environment configuration documentation and technical guides
- Add GitHub CLI usage instructions
- Include changelog references
- Enhance front-end interactivity documentation
- Add comprehensive Makefile comments

#### Dependencies

- Update packages for compatibility with Python 3.9.21 and Django 4.1.13
- Downgrade matplotlib version for compatibility
- Revise environment variable configurations in .env.vault
- Include pre-commit dependency in requirements.txt

### Related Issues

- Closes #33, #41
- [Add any other relevant issues here]

### Testing Performed

- Comprehensive test suite execution with pytest
- Manual testing of new company management features
- User profile functionality verification
- Chatbot interaction testing
- Theme switching and accessibility compliance validation
- Cross-browser compatibility testing

### Deployment Notes

- Contains multiple database migrations
- Requires updated environment variables via .env.vault
- Updated dependency requirements need to be installed
- Sentry integration requires configuration of Sentry DSN

### Contributors

- [agallo](https://github.com/enveng-group)
- [JaredStanbrook](https://github.com/JaredStanbrook)
- [cameronsims](https://github.com/cameronsims)
- [Channing88](https://github.com/Channing88)
- [muhammadhaseebahmad](https://github.com/mhahmad0)
