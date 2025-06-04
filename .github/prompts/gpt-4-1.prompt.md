<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [GitHub Copilot Prompt Template: constants.py Analysis and Recommendation Across All Apps](#github-copilot-prompt-template-constantspy-analysis-and-recommendation-across-all-apps)
  - [Goal](#goal)
  - [Context](#context)
  - [Objectives](#objectives)
  - [Sources](#sources)
  - [Expectations](#expectations)
  - [Acceptance Criteria](#acceptance-criteria)
  - [Instructions](#instructions)
  - [Additional Guidelines](#additional-guidelines)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

---

description:
Prompt for Copilot to analyze all apps in the Greenova project and determine which would benefit from having a constants.py file for project-wide or app-specific constants and enumerations. The output should recommend which apps should have a constants.py created, with reasoning for each recommendation, following project coding standards.
mode: agent

tools:

- context7 # REQUIRED: Use for all context and background information
- json
- git
- fetch # REQUIRED: Use for all web content retrieval (e.g., documentation, reports)
- filesystem # REQUIRED: Use for all file reading, writing, and editing
- sequential-thinking # REQUIRED: Use for all planning, reasoning, and stepwise logic
- github

---

# GitHub Copilot Prompt Template: constants.py Analysis and Recommendation Across All Apps

## Goal

Analyze all apps in the Greenova project (auditing, authentication, chatbot, company, core, dashboard, feedback, greenova, landing, mechanisms, obligations, procedures, projects, reports, responsibility, settings, static, templates, themes, users) and determine which would benefit from having a constants.py file for project-wide or app-specific constants and enumerations. Recommend which apps should have a constants.py created, with reasoning for each recommendation.

## Context

- Greenova is a modular Django project with multiple apps, each potentially containing constants or enumerations used in models, forms, views, or templates.
- Project standards encourage the use of constants.py for project-wide or app-specific constants and enumerations, as outlined in the code generation guidelines.
- Not all apps may require a constants.py; only recommend where it would improve maintainability, clarity, or code reuse.
- Recommendations should be based on actual code structure, presence of hardcoded values, repeated literals, or potential for shared enumerations.

## Objectives

- Scan all relevant code in each app for:
  - Hardcoded values or magic numbers/strings used in multiple places
  - Enumerations or choices used in models, forms, or business logic
  - Opportunities to centralize constants for clarity and maintainability
- For each app, determine if a constants.py would be beneficial
- Provide a list of apps that should have a constants.py, with a brief justification for each
- Do not create or modify any files; only provide analysis and recommendations

## Sources

- All relevant code in the following apps:
  - auditing/
  - authentication/
  - chatbot/
  - company/
  - core/
  - dashboard/
  - feedback/
  - greenova/
  - landing/
  - mechanisms/
  - obligations/
  - procedures/
  - projects/
  - reports/
  - responsibility/
  - settings/
  - static/
  - templates/
  - themes/
  - users/
- Project coding standards and code generation guidelines (context7)

## Expectations

- Use all available MCP servers to:
  - Analyze code structure and usage patterns in each app
  - Identify opportunities for centralizing constants and enumerations
  - Reference project standards for when to create constants.py
  - Provide clear, actionable recommendations
- Do not make any code changes; only output analysis and recommendations

## Acceptance Criteria

- [ ] Each app is evaluated for the need for a constants.py
- [ ] Recommendations are provided only where justified
- [ ] Each recommendation includes a brief explanation
- [ ] No code is changed or created
- [ ] Output is clear, actionable, and standards-compliant

## Instructions

- Use the filesystem and context7 MCP servers to analyze all relevant code
- For each app, state whether a constants.py is recommended, and why
- Summarize findings in a clear, organized list
- Do not create or modify any files
- Ensure recommendations align with project coding standards

## Additional Guidelines

- Only recommend constants.py where it will improve code organization, reduce duplication, or clarify enumerations
- Reference project standards and code generation guidelines as needed
- Use context7 and fetch for documentation lookups as needed
