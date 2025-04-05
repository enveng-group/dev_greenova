# GitHub Issue Template for Greenova Project

## Issue Type

{Choose one: Bug, Feature Request, Enhancement, Documentation, Test,
Refactoring}

## Issue Details

### Title

Create a concise title following the format `{type}: {summary}`

For bugs, use: `bug: {brief summary of the issue}` Example:
`bug: Dashboard fails to load environmental metrics with project filter`

### Description

A clear summary of the issue or feature request. For bugs, this should match
the bug report summary.

### Current Behavior

For bugs:

- What currently happens (from the "Actual Result" in bug report)
- Include specific error messages if applicable
- Reference error details from the bug report

For features/enhancements:

- Describe current limitations or missing functionality

### Expected Behavior

What should happen instead. For bugs, this comes directly from the "Expected
Result" section of the bug report.

### Steps to Reproduce (for bugs)

1. {First Step}
2. {Second Step}
3. {Additional Steps...}

Copy these directly from the bug report's "Steps to Reproduce" section.

### Environment Details

From the bug report's "Environment" section:

- **Application Version**: {Version number}
- **Operating System**: {OS and version}
- **Browser**: {Browser name and version, if applicable}
- **Device**: {Device type/model}

### Technical Context

- **Django Version**: 4.1.13
- **Python Version**: 3.9.21
- **Frontend Technologies**: PicoCSS, django-hyperscript, django-htmx
- **Database**: SQLite3 (development)
- **Affected Module/App**: {Specify the Django app affected}
- **Template Type/File**: {Specify if Jinja2 (.jinja) or DTL (.html) and the
  affected template file}
- **Template Engine**: {Jinja2 or Django Template Language}

### Logs and Error Details

- **Error Messages**: {Exact error text from bug report}
- **Traceback Summary**: {Brief summary of the most relevant parts of the
  traceback}
- **Reference**: Detailed traceback available in original bug report

### Impact Assessment

- **Severity**: {Critical/High/Medium/Low} (from bug report)
- **User Impact**: {Description of how users are affected}
- **Frequency**: {How often the issue occurs, from bug report}

### Visual Evidence

Reference any screenshots or videos from the bug report.

### Proposed Implementation

For bugs:

- Outline potential fix approach based on bug analysis
- Reference any identified cause from bug report

For features/enhancements:

- Outline a potential approach following project principles:
  - HTML-first approach with semantic markup
  - Progressive enhancement using our technology stack
  - Data-oriented programming principles
  - WCAG 2.1 AA compliance

### Acceptance Criteria

- [ ] Issue is resolved with no regressions
- [ ] Documentation is updated if necessary
- [ ] Tests are added/updated to cover the fix
- [ ] WCAG 2.1 AA compliance maintained
- [ ] {Additional criteria specific to this issue}

### Related Issues/PRs

Link any related issues or pull requests mentioned in the bug report.

### Workarounds

Document any temporary solutions mentioned in the bug report.

## Labels

Suggested labels (select all that apply):

- **Primary label**: `bug`, `enhancement`, `documentation`, etc.
- **Component labels**: `django`, `javascript`, `css`, `ui`, `database`, etc.
- **Priority labels**: `priority-critical`, `priority-high`, `priority-medium`,
  `priority-low`
- **Type labels**: `testing`, `refactoring`, `ux`, etc.

### Available Labels

- **bug**: Something isn't working
- **documentation**: Improvements or additions to documentation
- **duplicate**: This issue or pull request already exists
- **enhancement**: New feature or request
- **good first issue**: Good for newcomers
- **help wanted**: Extra attention is needed
- **invalid**: This doesn't seem right
- **question**: Further information is requested
- **wontfix**: This will not be worked on
- **javascript**: JavaScript-related issues
- **django**: Django framework issues
- **eslint**: ESLint configuration issues
- **makefile**: Makefile-related issues
- **docker**: Docker/Devcontainer issues
- **css**: CSS/styling issues
- **ui**: User interface issues
- **refactoring**: Code refactoring
- **ux**: User experience issues
- **pytest**: Pytest-related issues
- **selenium**: Selenium-related issues
- **testing**: General testing issues
- **authentication**: Authentication issues
- **django-allauth**: Issues related to django-allauth
- **database**: Database-related issues
- **accessibility**: Accessibility concerns
- **security**: Security concerns

---

**Reminder**: Please ensure all code contributions follow our development
practices:

- Test-driven development
- WCAG 2.1 AA accessibility standards
- Proper model relationships and constraints
- Class-based views with minimal mixins
- Type annotations with mypy
