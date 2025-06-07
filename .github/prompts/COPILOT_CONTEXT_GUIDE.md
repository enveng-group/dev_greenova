<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Essential Context Files for GitHub Copilot Agents](#essential-context-files-for-github-copilot-agents)
  - [1. Project Structure & Business Logic](#1-project-structure--business-logic)
  - [2. Configuration Files](#2-configuration-files)
  - [3. Django Core Files](#3-django-core-files)
  - [4. Standards & Guidelines](#4-standards--guidelines)
  - [5. Data & Schema Files](#5-data--schema-files)
  - [6. Frontend Configuration](#6-frontend-configuration)
  - [7. Quality & Testing](#7-quality--testing)
  - [8. Template & Static Structure Examples](#8-template--static-structure-examples)
  - [App-Specific Context Priority](#app-specific-context-priority)
  - [Recommended Context Files for Each App/Prompt](#recommended-context-files-for-each-appprompt)
    - [Core App (`core`)](#core-app-core)
    - [Obligations App (`obligations`)](#obligations-app-obligations)
    - [Projects App (`projects`)](#projects-app-projects)
    - [Mechanisms App (`mechanisms`)](#mechanisms-app-mechanisms)
    - [Responsibilities App (`responsibilities`)](#responsibilities-app-responsibilities)
    - [Audits App (`audits`)](#audits-app-audits)
    - [Procedures App (`procedures`)](#procedures-app-procedures)
    - [Reporting App (`reporting`)](#reporting-app-reporting)
    - [Dashboard App (`dashboard`)](#dashboard-app-dashboard)
    - [Company App (`company`)](#company-app-company)
    - [Chatbot App (`chatbot`)](#chatbot-app-chatbot)
    - [Feedback App (`feedback`)](#feedback-app-feedback)
    - [Navigation App (`navigation`)](#navigation-app-navigation)
    - [Sidebar App (`sidebar`)](#sidebar-app-sidebar)
    - [Protobuf App (`protobuf`)](#protobuf-app-protobuf)
    - [Landing App (`landing`)](#landing-app-landing)
  - [Usage Instructions for Copilot Agents](#usage-instructions-for-copilot-agents)
  - [Critical Notes](#critical-notes)
  - [Standard File Patterns](#standard-file-patterns)
  - [Recommended GitHub Copilot Agent for Each Prompt](#recommended-github-copilot-agent-for-each-prompt)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Essential Context Files for GitHub Copilot Agents

To ensure accurate and context-aware code generation and refactoring, always provide the following files as context when using any Greenova app prompt:

## 1. Project Structure & Business Logic

- `greenova_project_tree.log`: The complete current file and directory structure.
- `Greenova-Workflow.bpmn`: The business process workflow definitions for the entire system.
- `00_app_ecosystem_overview.md`: Overview of app relationships and dependencies.
- `APP_CONSOLIDATION_SUMMARY.md`: Details on deprecated apps and consolidation status.

## 2. Configuration Files

- `pyproject.toml`: Python project configuration and dependencies.
- `package.json`: Node.js dependencies and build scripts.
- `requirements.txt`, `uv.lock`: Python dependencies and lock file.
- `.env`: Environment variables.
- `.nvmrc`, `.npmrc`: Node.js and npm configuration.

## 3. Django Core Files

- `greenova/settings.py`: Django settings.
- `greenova/urls.py`: Root URL configuration.
- `manage.py`: Django management script.

## 4. Standards & Guidelines

- `copilot-instructions.md`: Complete coding standards and guidelines.
- `python_startup.py`: Python development environment setup.

## 5. Data & Schema Files

- All `*/proto/*.proto` files: Protocol Buffer definitions for each app.
- All `*/models.py` files: Django model definitions.
- Any `schema.json` or `data.json` files: Data schema and sample data.

## 6. Frontend Configuration

- `core/static/core/scss/main.scss`: Main SCSS entry point.
- `core/static/core/ts/tsconfig.json`: TypeScript configuration.
- `core/static/core/as/asconfig.json`: AssemblyScript configuration.

## 7. Quality & Testing

- `.pre-commit-config.yaml`: Pre-commit hooks configuration.
- `ruff.toml`: Python linting configuration.
- `mypy.ini`: Type checking configuration.
- `pytest.ini`: Testing configuration.

## 8. Template & Static Structure Examples

- `core/templates/core/base.html`: Base template structure.
- `dashboard/templates/dashboard/`: Example app templates.
- `obligations/templates/obligations/`: Complex app templates.

## App-Specific Context Priority

- For core apps (`core`, `navigation`, `sidebar`, `protobuf`): Always include all configuration files, the full core app structure, and business process workflow.
- For business process apps (`obligations`, `projects`, `dashboard`, etc.): Include all configuration files, core base template, core models, the app's current structure, and related dependencies.
- For support apps (`chatbot`, `feedback`, `landing`): Include configuration files, core templates/models, and the app's current structure.

## Recommended Context Files for Each App/Prompt

Below are the most important files and directories to include as context for each major Greenova app or prompt. Always include these, in addition to the global context files listed above.

### Core App (`core`)

- `core/models.py`, `core/forms.py`, `core/views.py`, `core/admin.py`, `core/urls.py`, `core/serializers.py`, `core/permissions.py`, `core/context_processors.py`, `core/constants.py`, `core/utils.py`, `core/mixins.py`, `core/tables.py`, `core/filters.py`, `core/templates/core/`, `core/static/core/`, `core/tests.py`, `core/types.py`, `core/py.typed`

### Obligations App (`obligations`)

- `obligations/models.py`, `obligations/forms.py`, `obligations/views.py`, `obligations/admin.py`, `obligations/urls.py`, `obligations/serializers.py`, `obligations/permissions.py`, `obligations/constants.py`, `obligations/utils.py`, `obligations/tables.py`, `obligations/filters.py`, `obligations/templates/obligations/`, `obligations/static/obligations/`, `obligations/tests.py`, `obligations/types.py`, `obligations/py.typed`, `obligations/proto/obligations.proto`, `obligations/proto_utils.py`

### Projects App (`projects`)

- `projects/models.py`, `projects/forms.py`, `projects/views.py`, `projects/admin.py`, `projects/urls.py`, `projects/serializers.py`, `projects/permissions.py`, `projects/constants.py`, `projects/utils.py`, `projects/tables.py`, `projects/filters.py`, `projects/templates/projects/`, `projects/static/projects/`, `projects/tests.py`, `projects/types.py`, `projects/py.typed`, `projects/proto/projects.proto`, `projects/proto_utils.py`

### Mechanisms App (`mechanisms`)

- `mechanisms/models.py`, `mechanisms/forms.py`, `mechanisms/views.py`, `mechanisms/admin.py`, `mechanisms/urls.py`, `mechanisms/serializers.py`, `mechanisms/permissions.py`, `mechanisms/constants.py`, `mechanisms/utils.py`, `mechanisms/tables.py`, `mechanisms/filters.py`, `mechanisms/templates/mechanisms/`, `mechanisms/static/mechanisms/`, `mechanisms/tests.py`, `mechanisms/types.py`, `mechanisms/py.typed`, `mechanisms/proto/mechanism.proto`, `mechanisms/proto_utils.py`

### Responsibilities App (`responsibilities`)

- `responsibilities/models.py`, `responsibilities/forms.py`, `responsibilities/views.py`, `responsibilities/admin.py`, `responsibilities/urls.py`, `responsibilities/serializers.py`, `responsibilities/permissions.py`, `responsibilities/constants.py`, `responsibilities/utils.py`, `responsibilities/tables.py`, `responsibilities/filters.py`, `responsibilities/templates/responsibilities/`, `responsibilities/static/responsibilities/`, `responsibilities/tests.py`, `responsibilities/types.py`, `responsibilities/py.typed`, `responsibilities/proto_utils.py`

### Audits App (`audits`)

- `audits/models.py`, `audits/forms.py`, `audits/views.py`, `audits/admin.py`, `audits/urls.py`, `audits/serializers.py`, `audits/permissions.py`, `audits/constants.py`, `audits/utils.py`, `audits/tables.py`, `audits/filters.py`, `audits/templates/audits/`, `audits/static/audits/`, `audits/tests.py`, `audits/types.py`, `audits/py.typed`, `audits/proto_utils.py`

### Procedures App (`procedures`)

- `procedures/models.py`, `procedures/forms.py`, `procedures/views.py`, `procedures/admin.py`, `procedures/urls.py`, `procedures/serializers.py`, `procedures/permissions.py`, `procedures/constants.py`, `procedures/utils.py`, `procedures/tables.py`, `procedures/filters.py`, `procedures/templates/procedures/`, `procedures/static/procedures/`, `procedures/tests.py`, `procedures/types.py`, `procedures/py.typed`, `procedures/proto_utils.py`

### Reporting App (`reporting`)

- `reporting/views.py`, `reporting/utils.py`, `reporting/urls.py`, `reporting/templates/reporting/`, `reporting/services.py`, `reporting/static/reporting/`, `reporting/tests.py`, `reporting/py.typed`

### Dashboard App (`dashboard`)

- `dashboard/views.py`, `dashboard/forms.py`, `dashboard/urls.py`, `dashboard/templates/dashboard/`, `dashboard/static/dashboard/`, `dashboard/tests.py`, `dashboard/py.typed`

### Company App (`company`)

- `company/models.py`, `company/forms.py`, `company/views.py`, `company/admin.py`, `company/urls.py`, `company/serializers.py`, `company/permissions.py`, `company/constants.py`, `company/utils.py`, `company/mixins.py`, `company/templates/company/`, `company/static/company/`, `company/tests.py`, `company/types.py`, `company/py.typed`, `company/proto/company.proto`, `company/proto_utils.py`

### Chatbot App (`chatbot`)

- `chatbot/models.py`, `chatbot/forms.py`, `chatbot/views.py`, `chatbot/admin.py`, `chatbot/urls.py`, `chatbot/serializers.py`, `chatbot/permissions.py`, `chatbot/constants.py`, `chatbot/utils.py`, `chatbot/services.py`, `chatbot/templates/chatbot/`, `chatbot/static/chatbot/`, `chatbot/tests.py`, `chatbot/types.py`, `chatbot/py.typed`, `chatbot/proto/chatbot.proto`, `chatbot/proto_utils.py`

### Feedback App (`feedback`)

- `feedback/models.py`, `feedback/forms.py`, `feedback/views.py`, `feedback/admin.py`, `feedback/urls.py`, `feedback/serializers.py`, `feedback/permissions.py`, `feedback/constants.py`, `feedback/utils.py`, `feedback/templates/feedback/`, `feedback/static/feedback/`, `feedback/tests.py`, `feedback/types.py`, `feedback/py.typed`, `feedback/proto/feedback.proto`, `feedback/proto_utils.py`

### Navigation App (`navigation`)

- `navigation/models.py`, `navigation/views.py`, `navigation/forms.py`, `navigation/urls.py`, `navigation/templates/navigation/`, `navigation/static/navigation/`, `navigation/tests.py`, `navigation/py.typed`

### Sidebar App (`sidebar`)

- `sidebar/models.py`, `sidebar/views.py`, `sidebar/forms.py`, `sidebar/urls.py`, `sidebar/templates/sidebar/`, `sidebar/static/sidebar/`, `sidebar/tests.py`, `sidebar/py.typed`

### Protobuf App (`protobuf`)

- `protobuf/models.py`, `protobuf/views.py`, `protobuf/urls.py`, `protobuf/templates/protobuf/`, `protobuf/static/protobuf/`, `protobuf/tests.py`, `protobuf/py.typed`, all `.proto` files in `protobuf/`

### Landing App (`landing`)

- `landing/views.py`, `landing/forms.py`, `landing/urls.py`, `landing/templates/landing/`, `landing/static/landing/`, `landing/tests.py`, `landing/py.typed`

## Usage Instructions for Copilot Agents

1. Start by reading the app ecosystem overview and consolidation summary.
2. Always include configuration files for dependency and environment context.
3. Reference the business workflow to understand the app's business purpose.
4. Check the project tree to understand the current file structure before making changes.
5. Follow coding standards from copilot-instructions.md strictly.
6. Use the core app as the foundation reference for all other apps.

## Critical Notes

- The `users` and `auditing` apps are deprecated and consolidated into `core`.
- All apps must use `core` for authentication, user management, and audit services.
- All apps must include `navigation` and `sidebar` components.
- Protocol Buffers are managed centrally in the `protobuf` app.
- No JavaScript allowed—use django-hyperscript and django-htmx instead.

## Standard File Patterns

When working with any app, expect these standard file patterns:

- `models.py`: Django models
- `views.py`: Django views
- `forms.py`: Django forms
- `urls.py`: URL routing
- `admin.py`: Django admin
- `templates/{app_name}/`: App templates
- `static/{app_name}/`: App static files
- `proto/{app_name}.proto`: Protocol Buffer definitions
- `serializers.py`: Protobuf serialization
- `proto_utils.py`: Protocol Buffer utilities
- `management/commands/`: Django management commands
- `tests.py` or `test_{app_name}.py`: Unit tests

## Recommended GitHub Copilot Agent for Each Prompt

| Prompt/App Type                                                                                                       | Best Agent | Rationale                                                                        |
| --------------------------------------------------------------------------------------------------------------------- | ---------- | -------------------------------------------------------------------------------- |
| Core app, consolidation, globals                                                                                      | GPT-4o     | Best for complex, cross-app refactoring, deep context, and standards enforcement |
| Business process apps (obligations, projects, dashboard, audits, reporting, mechanisms, responsibilities, procedures) | GPT-4o     | Handles multi-file, multi-model, and workflow logic well                         |
| Protobuf app, serialization                                                                                           | GPT-4o     | Handles protocol buffer, code generation, and cross-language serialization       |
| Navigation/sidebar setup                                                                                              | GPT-4o     | UI/UX structure, template inheritance, and context awareness                     |
| Chatbot, feedback, landing                                                                                            | GPT-4o     | Conversational, support, and user-facing logic; strong context retention         |
| Company app                                                                                                           | GPT-4o     | Multi-tenant, user/org context, and permissions                                  |
| Static/Frontend/SCSS/AssemblyScript                                                                                   | GPT-4o     | Frontend build, SCSS, and AssemblyScript code generation                         |
| Shell scripts, DevOps, CI/CD                                                                                          | GPT-4o     | Shell, YAML, and automation tasks                                                |

- **GPT-4o**: Use for all Greenova prompts and tasks. It provides the best overall results for complex, multi-app, and standards-driven refactoring, as well as frontend, backend, and DevOps tasks.

Always use GPT-4o for Greenova unless a specific exception is documented.
