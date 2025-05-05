# Pull Request: Release v0.0.6

## Title

`release(v0.0.6): Company management, authentication & auditing system enhancements`

## Description

### Purpose

This PR delivers pre-release v0.0.6 which integrates multiple feature branches
and infrastructure improvements across the Greenova platform. This release
focuses on company management capabilities, authentication enhancements,
improved development workflows, and better data management tooling.

### Changes

#### Authentication Framework

- Implemented proper authentication namespace in URLs.py
- Added correct namespace routing for login redirects
- Configured LOGIN_URL setting to use authentication namespace
- Fixed test_company_create_requires_login test

#### Company Management Module

- Added Company and UserCompany models with proper relationships
- Implemented company-scoped data access control
- Created middleware for active company context
- Added mixins for company-scoped views
- Enhanced company templates with improved UI components

#### Auditing Module

- Created dedicated auditing app for compliance and non-conformance tracking
- Extracted comments into standalone models for better data management
- Added admin interface for audit record management
- Implemented history tracking for key operations

#### Development Workflow

- Added IPython integration with autoreload capabilities
- Added bash aliases for improved developer workflow
- Enhanced VSCode tasks.json for improved development workflow
- Migrated to dotenv-vault for more secure environment management
- Rebuilt django-build command in Makefile

#### Data Management

- Refactored obligation import command for improved reliability
- Enhanced error handling and reporting during imports
- Added transaction support to prevent partial imports
- Improved progress reporting and logging

#### User Experience

- Added interactive hyperlinks for status counts in procedure views
- Enhanced user profile functionality with role relationship display
- Added overdue actions display to user dashboard
- Improved data filtering with HTMX for dynamic content loading

### Related Issues

- Fixes #72 - Authentication namespace implementation
- Fixes #87 - Company management module
- Fixes #88 - Obligation import improvements
- Fixes #37 - Auditing module implementation

### Testing Performed

- Comprehensive test suite execution with pytest
- Verified proper authentication flow with login redirects
- Tested company management features with multi-company scenarios
- Validated obligation import process with error handling
- Verified audit record creation and management
- Tested integration between company and obligation models
- Validated development environment configuration

### Deployment Notes

- Contains database migrations for company model and auditing module
- Requires updated environment variables via `.env.vault`
- Updated dependency requirements in requirements.txt
- Includes infrastructure changes for development workflow

### Contributors

- [agallo](https://github.com/enveng-group)
- [JaredStanbrook](https://github.com/JaredStanbrook)
- [mhahmad0](https://github.com/mhahmad0)
- [Channing88](https://github.com/Channing88)
- [camersonsims](https://github.com/camersonsims)
- [alexcao123456](https://github.com/alexcao123456)
