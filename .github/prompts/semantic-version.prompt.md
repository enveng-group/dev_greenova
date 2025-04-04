# Semantic Versioning Guide for Greenova Project

When advising on version numbers for Greenova releases, use this guide to
determine the appropriate version increment based on the changes made.

## Core Semantic Versioning Principles

Greenova follows the Semantic Versioning 2.0.0 specification, which defines
version numbers in the format of MAJOR.MINOR.PATCH (e.g., 1.2.3).

- **MAJOR**: Increment when making incompatible API changes
- **MINOR**: Increment when adding functionality in a backwards-compatible
  manner
- **PATCH**: Increment when making backwards-compatible bug fixes

## When to Increment Each Version Component

### MAJOR Version (X.y.z)

Increment when:

- Changes break backward compatibility
- Significant API changes that require consumers to modify their code
- Dropping support for older dependencies (e.g., Python 3.8)
- Architectural changes that alter how the application functions
- Database schema changes that require migrations with data transformation

Examples for Greenova:

- Changing the structure of the Obligation model in a way that breaks existing
  code
- Replacing django-allauth with a different authentication system
- Upgrading from Django 4.x to Django 5.x with breaking changes

### MINOR Version (x.Y.z)

Increment when:

- Adding new features in a backwards-compatible manner
- Adding new models, views, or endpoints
- Deprecating functionality (but not removing it)
- Adding new dependencies that don't require changes to existing code
- Significant performance improvements

Examples for Greenova:

- Adding a new model for tracking compliance metrics
- Implementing a new dashboard with additional visualizations
- Adding support for new environmental compliance categories
- Enhancing existing API endpoints with new optional parameters

### PATCH Version (x.y.Z)

Increment when:

- Fixing bugs without changing the API
- Making performance improvements that don't affect functionality
- Updating documentation
- Refactoring code without changing behavior
- Security fixes that don't break compatibility

Examples for Greenova:

- Fixing calculation errors in environmental metrics
- Resolving UI issues in the compliance dashboard
- Correcting form validation errors
- Addressing security vulnerabilities in dependencies

## Python-Specific Versioning (PEP 440)

For Python packages and modules within Greenova, follow these additional
guidelines:

- Local version identifiers: `1.2.3+dev`, `1.2.3+git.5a7c8f9`
- Pre-releases: `1.2.3a1` (alpha), `1.2.3b1` (beta), `1.2.3rc1` (release
  candidate)
- Post-releases: `1.2.3.post1`
- Development releases: `1.2.3.dev1`

Example version sequence:

```
1.2.3.dev1 → 1.2.3a1 → 1.2.3a2 → 1.2.3b1 → 1.2.3rc1 → 1.2.3 → 1.2.3.post1
```

## NPM Package Versioning

For frontend packages in Greenova, follow these additional npm guidelines:

- Tilde ranges (`~1.2.3`): Allow patch updates
- Caret ranges (`^1.2.3`): Allow minor updates (most common)
- Pre-release tags: `1.2.3-alpha.1`, `1.2.3-beta.1`, `1.2.3-rc.1`

## Pre-release and Build Metadata

### Pre-release Versions

Format: `MAJOR.MINOR.PATCH-[pre-release identifier]`

Examples:

- `1.4.0-alpha.1` - First alpha of version 1.4.0
- `2.0.0-beta.2` - Second beta of version 2.0.0
- `1.5.2-rc.1` - First release candidate for 1.5.2

Use for:

- Testing significant changes before a formal release
- Getting feedback on new features
- Allowing early adopters to try new functionality

### Build Metadata

Format: `MAJOR.MINOR.PATCH+[build metadata]`

Examples:

- `1.3.5+20230615` - Build from June 15, 2023
- `2.0.1+git.a1b2c3d` - Build from git commit a1b2c3d

Use for:

- Identifying specific builds
- Including CI/CD information
- Referencing internal build numbers

## Decision Process for Greenova Releases

When determining the next version number for a Greenova release:

1. Review all changes since the last release
2. Categorize each change as MAJOR, MINOR, or PATCH
3. Choose the highest category of change to increment
4. Reset all lower-significance numbers to zero when incrementing a
   higher-significance number
5. Add pre-release identifiers for testing releases
6. Add build metadata if needed for tracking specific builds

## Examples Applied to Greenova

### Example 1: Bug Fix Release

Current version: 1.2.3 Changes:

- Fixed issue with obligation due date calculations
- Updated documentation for environmental compliance tracking
- Optimized database queries for better performance Next version: 1.2.4 (PATCH
  increment)

### Example 2: Feature Release

Current version: 1.2.4 Changes:

- Added new dashboard for compliance analytics
- Implemented new notification system for upcoming obligations
- Added export functionality for compliance reports Next version: 1.3.0 (MINOR
  increment, reset PATCH)

### Example 3: Breaking Change Release

Current version: 1.3.2 Changes:

- Refactored Obligation model with new required fields
- Upgraded from Django 4.1 to Django 5.0
- Changed authentication flow for compliance officials Next version: 2.0.0
  (MAJOR increment, reset MINOR and PATCH)

## References

[1] Semantic Versioning 2.0.0, "Semantic Versioning Specification," SemVer.org.
[Online]. Available: <https://semver.org/> [Accessed: Apr. 2025].

[2] Python Enhancement Proposal 440, "Version Identification and Dependency
Specification," Python.org, 2015. [Online]. Available:
<https://peps.python.org/pep-0440/> [Accessed: Apr. 2025].

[3] "Version Schema," VersionSchema.org. [Online]. Available:
<https://versionschema.org/> [Accessed: Apr. 2025].

[4] npm Inc., "About Semantic Versioning," npm Documentation. [Online].
Available: <https://docs.npmjs.com/about-semantic-versioning> [Accessed: Oct.
2023].
