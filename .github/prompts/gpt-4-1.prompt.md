<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [GitHub Copilot Prompt Template: utils.py (General-Purpose Utility Functions) Analysis and Recommendation Across All Apps](#github-copilot-prompt-template-utilspy-general-purpose-utility-functions-analysis-and-recommendation-across-all-apps)
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
Prompt for Copilot to analyze all apps in the Greenova project and determine which would benefit from having a utils.py module for general-purpose utility functions. The output should recommend which apps should have a utils.py created, with reasoning for each recommendation, following project coding standards.
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

# GitHub Copilot Prompt Template: utils.py (General-Purpose Utility Functions) Analysis and Recommendation Across All Apps

## Goal

Analyze all apps in the Greenova project (auditing, authentication, chatbot, company, core, dashboard, feedback, greenova, landing, mechanisms, obligations, procedures, projects, reports, responsibility, settings, static, templates, themes, users) and determine which would benefit from having a utils.py module for general-purpose utility functions. Recommend which apps should have a utils.py created, with reasoning for each recommendation.

## Context

- Greenova is a modular Django project with multiple apps, each potentially containing logic that could be clarified or improved by centralizing general-purpose utility functions in a utils.py module.
- Project standards encourage the use of utils.py for reusable, app-specific utility functions, as outlined in the code generation guidelines.
- Not all apps may require a utils.py; only recommend where it would improve maintainability, enable reuse, or clarify utility logic.
- Recommendations should be based on actual code structure, presence of repeated or general-purpose helper functions, and project requirements.

## Objectives

- Scan all relevant code in each app for:
  - Presence of repeated, general-purpose, or helper functions (e.g., formatting, parsing, conversions, calculations)
  - Opportunities to centralize and reuse utility logic for clarity and maintainability
  - Existing utility functions defined in other files (e.g., models, views)
- For each app, determine if a utils.py (with general-purpose utility functions) would be beneficial
- Provide a list of apps that should have a utils.py, with a brief justification for each
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
  - Identify opportunities for centralizing reusable utility functions
  - Reference project standards for when to create utils.py
  - Provide clear, actionable recommendations
- Do not make any code changes; only output analysis and recommendations

## Acceptance Criteria

- [ ] Each app is evaluated for the need for a utils.py module
- [ ] Recommendations are provided only where justified
- [ ] Each recommendation includes a brief explanation
- [ ] No code is changed or created
- [ ] Output is clear, actionable, and standards-compliant

## Instructions

- Use the filesystem and context7 MCP servers to analyze all relevant code
- For each app, state whether a utils.py is recommended, and why
- Summarize findings in a clear, organized list
- Do not create or modify any files
- Ensure recommendations align with project coding standards

## Additional Guidelines

- Only recommend utils.py where it will improve code organization, enable reusable utility logic, or clarify helper function usage
- Reference project standards and code generation guidelines as needed
- Use context7 and fetch for documentation lookups as needed
