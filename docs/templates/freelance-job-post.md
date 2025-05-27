# Freelance Django Developer Needed: Greenova Environmental Compliance Platform

## Project Overview

Greenova is an open-source Django web application for environmental
professionals to track, manage, and report on environmental obligations and
compliance requirements. The platform is modular, extensible, and currently at
the proof-of-concept stage. We are seeking a Django development firm or
experienced freelancers to help advance the project to production readiness.

## Project Goals

- Deliver a robust, maintainable proof-of-concept for stakeholders and
  outsourcing partners
- Achieve high code quality, documentation, and test coverage
- Implement features and improvements as outlined in the
  [project roadmap](https://github.com/enveng-group/dev_greenova/blob/main/docs/ROADMAP.md)
  and open issues

## Technical Stack & Skills Required

- **Backend**: Python 3.12.9, Django 5.2
- **Frontend**: Semantic HTML5, PicoCSS (classless), django-hyperscript,
  django-htmx
- **Database**: SQLite3 (development/production)
- **Other**: Protobuf3 for data serialization, SASS/PostCSS,
  TypeScript/AssemblyScript (as needed)
- **Testing**: pytest, pytest-django, pytest-cov, pytest-xdist
- **Linting/Formatting**: ruff, pylint, djlint, markdownlint, stylelint,
  eslint, shellcheck, ruff-format, isort, prettier, shfmt
- **Type Checking**: mypy (strict), beartype (runtime), stubgen/stubtest for
  stubs

## Project Status

- Modular Django project with specialized apps
  ([see codebase](https://github.com/enveng-group/dev_greenova/tree/main/greenova))
- Core models, views, and forms for obligation tracking
- Initial API endpoints and admin interfaces
- Comprehensive documentation:
  - [README](https://github.com/enveng-group/dev_greenova/blob/main/README.md)
  - [Architecture](https://github.com/enveng-group/dev_greenova/blob/main/docs/ARCHITECTURE.md)
  - [API Documentation](https://github.com/enveng-group/dev_greenova/blob/main/docs/API_DOCUMENTATION.md)
  - [Testing](https://github.com/enveng-group/dev_greenova/blob/main/docs/TESTING.md)
  - [Roadmap](https://github.com/enveng-group/dev_greenova/blob/main/docs/ROADMAP.md)
  - [Style Guide](https://github.com/enveng-group/dev_greenova/blob/main/docs/style_guide.md)
  - [FAQ](https://github.com/enveng-group/dev_greenova/blob/main/docs/FAQ.md)
  - [CONTRIBUTING](https://github.com/enveng-group/dev_greenova/blob/main/CONTRIBUTING.md)
- Open issues and pull requests:
  [GitHub Issues](https://github.com/enveng-group/dev_greenova/issues),
  [Pull Requests](https://github.com/enveng-group/dev_greenova/pulls)

## Scope of Work

1. Log in using the credentials created during setup

   **Status:**

   - Login template and backend implemented; user model extended.
   - MFA and advanced error handling not yet present.

   **Gaps & Improvements:**

   - Integrate django-allauth for multi-factor authentication (MFA).
   - Refactor login template for accessibility (ARIA, focus management) and
     PicoCSS/classless style.
   - Add runtime type checking and Google-style docstrings to authentication
     views.
   - Write unit tests for login/logout flows.

   **Pseudocode:**

```pseudocode
Login flow:
  IF user visits login page THEN
    credentials := get user input
    IF credentials are valid THEN
      login user
      redirect to dashboard
    ELSE
      show error and retry
```

1. Create projects and define environmental mechanisms

   **Status:**

   - Project and Membership models implemented; EnvironmentalMechanism model
     exists.
   - Admin CRUD available; user-facing CRUD limited.

   **Gaps & Improvements:**

   - Add user-facing forms/views for project and mechanism creation.
   - Enforce project-mechanism relationships.
   - Refactor models for strict type annotations and docstrings.
   - Add PicoCSS styling and accessibility to forms.

   **Pseudocode:**

```pseudocode
Project and mechanism relationships:
  Project has many Memberships
  Project has many EnvironmentalMechanisms
  Membership links User to Project
  EnvironmentalMechanism belongs to Project
```

1. Add obligations related to your projects

   **Status:**

   - Obligation model and signals implemented; linked to projects and
     mechanisms.
   - Admin CRUD present; user-facing CRUD limited.

   **Gaps & Improvements:**

   - Implement user-facing obligation creation/editing forms.
   - Enforce validation (due dates, project linkage).
   - Add PicoCSS and accessibility improvements to forms.
   - Refactor for type annotations and docstrings.

   **Pseudocode:**

```pseudocode
Obligation relationships:
  Project has many Obligations
  EnvironmentalMechanism has many Obligations
  Obligation belongs to Project and EnvironmentalMechanism
```

1. Assign responsibilities to users

   **Status:**

   - ResponsibilityAssignment model links users to obligations/projects.
   - Admin interface present; user-facing assignment UI minimal.

   **Gaps & Improvements:**

   - Add user-facing forms/views for assigning responsibilities.
   - Enforce permission checks (only managers/admins can assign).
   - Refactor for type annotations, docstrings, and runtime type checking.

   **Pseudocode:**

```pseudocode
Responsibility assignment:
  ResponsibilityAssignment links User to Obligation
```

1. Monitor compliance status

   **Status:**

   - Dashboard shows compliance cards and status summaries.
   - Status logic in models and signals.

   **Gaps & Improvements:**

   - Add filtering and drill-down for compliance status.
   - Refactor dashboard for accessibility and semantic HTML.
   - Add ARIA live regions for dynamic updates.
   - Improve code documentation and type safety.

   **Pseudocode:**

```pseudocode
Compliance dashboard logic:
  status_cards := fetch compliance data
  display status cards
  IF user clicks card THEN
    show detail drilldown
  ELSE
    wait for interaction
```

1. CRUD user profiles and company information

   **Status:**

   - UserProfile, Company, and Membership models implemented.
   - Admin CRUD present; user-facing CRUD limited.

   **Gaps & Improvements:**

   - Add user-facing forms/views for profile and company CRUD.
   - Enforce permissions (users edit own profile, admins manage companies).
   - Refactor for type annotations, docstrings, and runtime type checking.

   **Pseudocode:**

```pseudocode
User profile and company relationships:
  User has UserProfile
  User has many Memberships
  Company has many Memberships
  Membership links User to Company
```

1. Drill down into mechanisms, then into procedures, then into obligations for
   detailed information

   - Perform CRUD operations on obligations

   **Status:**

   - Models for mechanisms, procedures, and obligations exist.
   - Some detail views present; drill-down navigation limited.
   - CRUD for obligations mostly in admin.

   **Gaps & Improvements:**

   - Implement user-facing drill-down navigation (mechanism → procedure →
     obligation).
   - Add detail views and breadcrumbs for navigation.
   - Procuedure charts need to display in interactive grid format.
   - Add filtering and sorting options for obligations.
   - Refactor for accessibility and semantic HTML.
   - Add CRUD forms/views for obligations.

   **Pseudocode:**

```pseudocode
Drill-down navigation:
  mechanism := select mechanism
  procedures := list procedures for mechanism
  procedure := select procedure
  obligations := list obligations for procedure
  view or edit obligation
```

1. When hovering over the overdue obligations card, a tooltip will display a
   list of overdue obligations

   **Status:**

   - Dashboard card for overdue obligations exists.
   - No tooltip or interactive list on hover; obligation detail/edit pages
     exist in admin.

   **Gaps & Improvements:**

   - Implement accessible tooltip using django-hyperscript or htmx.
   - List overdue obligations in tooltip, each linking to detail page.
   - Add user-facing CRUD for overdue obligations.
   - Refactor for accessibility (keyboard, ARIA).

   **Pseudocode:**

```pseudocode
Overdue obligations tooltip:
  IF hover over overdue card THEN
    overdue_list := get overdue obligations
    show tooltip with overdue_list
    IF click obligation in overdue_list THEN
      go to detail page
      edit obligation
```

- Each overdue obligation will be listed and clickable, linking to its detail
  page
- You can edit individual obligation records from their detail pages
- Full CRUD operations are supported for overdue obligations

1. Generate charts and data visualizations using matplotlib and Plotly:

   - Integrate static and interactive charts into dashboard and reporting views
     (compliance status, overdue obligations, project summaries)
   - Use matplotlib for server-side static reporting (SVG charts for reports,
     emails, server-rendered templates)
   - Use Plotly (Python SDK) for client-side, interactive, user-driven data
     exploration and compliance tracking
   - Use protobuf3 and django-pb-model for data serialization and transport
     between backend and frontend, especially for chart data and API endpoints
   - Ensure all visualizations are accessible (ARIA, keyboard navigation, color
     contrast) and follow project style guidelines
   - All documentation for charting and data visualization features must be
     written in reStructuredText (RST) format

1. Implement and maintain Protocol Buffer (protobuf3) schemas:

   - Use protobuf3 for data serialization between backend and any external
     systems or services
   - Ensure all protocol buffer definitions are versioned, documented, and
     tested
   - Integrate protobuf workflows into the Django project as per the
     architecture and requirements

1. Review and refactor existing codebase for maintainability, readability, and
   compliance with project standards

1. Implement missing features and resolve open issues as prioritized in the
   roadmap and GitHub tracker

1. Write and improve unit/integration tests to meet coverage requirements

1. Generate and validate type stubs for all internal modules

1. Ensure all code passes automated pre-commit checks (ruff, mypy, pylint,
   djlint, etc.)

1. Update and expand documentation as needed (RST format)

1. Prepare the project for handoff to a larger development team or firm

---

For each item, actionable tasks include:

- Refactor code for strict type annotations, Google-style docstrings, and
  beartype decorators
- Ensure all templates use semantic HTML, PicoCSS, and are accessible (WCAG 2.1
  AA)
- Add/expand unit and integration tests for all user-facing flows
- Document all new/updated modules and workflows per project standards
- Use diagrams and pseudocode in documentation and issues to clarify logic and
  data relationships

## Deliverables

- Refactored, well-documented Django codebase
- Passing pre-commit checks and CI pipeline
- 80%+ test coverage (100% for critical modules)
- Complete and validated type stubs (.pyi) and py.typed markers
- Updated documentation
  ([README](https://github.com/enveng-group/dev_greenova/blob/main/README.md),
  [API](https://github.com/enveng-group/dev_greenova/blob/main/docs/API_DOCUMENTATION.md),
  [Architecture](https://github.com/enveng-group/dev_greenova/blob/main/docs/ARCHITECTURE.md),
  [Testing](https://github.com/enveng-group/dev_greenova/blob/main/docs/TESTING.md),
  etc.)
- Summary report of changes, recommendations, and next steps

## Timeline & Hiring Process

- **Anticipated hire date:** Immediately (project kick-off scheduled for
  Monday, 26th May 2025)
- **Project due date:** 6th June 2025
- Applications reviewed for technical fit, code quality, and communication
- Shortlisted candidates may be asked to complete a small code review or test
  task
- Final selection based on technical merit, communication, and alignment with
  project goals

## Application Instructions

- Include a brief summary of your relevant experience and approach to Django
  code quality
- Reference similar projects or contributions (links preferred)
- Propose an initial review and onboarding plan
- Indicate your availability and estimated timeline for the first phase

## References & Resources

- [Project README](https://github.com/enveng-group/dev_greenova/blob/main/README.md)
- [Contributing Guide](https://github.com/enveng-group/dev_greenova/blob/main/CONTRIBUTING.md)
- [API Documentation](https://github.com/enveng-group/dev_greenova/blob/main/docs/API_DOCUMENTATION.md)
- [Architecture](https://github.com/enveng-group/dev_greenova/blob/main/docs/ARCHITECTURE.md)
- [Testing](https://github.com/enveng-group/dev_greenova/blob/main/docs/TESTING.md)
- [Roadmap](https://github.com/enveng-group/dev_greenova/blob/main/docs/ROADMAP.md)
- [Style Guide](https://github.com/enveng-group/dev_greenova/blob/main/docs/style_guide.md)
- [FAQ](https://github.com/enveng-group/dev_greenova/blob/main/docs/FAQ.md)
- [GitHub Issues](https://github.com/enveng-group/dev_greenova/issues)
- [GitHub Pull Requests](https://github.com/enveng-group/dev_greenova/pulls)

## Additional Information

- License: AGPL-3.0
- Author: Adrian Gallo
  ([agallo@enveng-group.com.au](mailto:agallo@enveng-group.com.au))
- All work must comply with project documentation, style guides, and
  accessibility requirements
- For questions, review the
  [FAQ](https://github.com/enveng-group/dev_greenova/blob/main/docs/FAQ.md) or
  open an issue on GitHub

---

_This job post was generated based on the Greenova project documentation,
roadmap, and
[Upwork job posting best practices](https://www.upwork.com/resources/how-to-post-job-on-upwork).
For full project context, see the linked documentation and GitHub repository._
