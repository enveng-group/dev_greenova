<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [GitHub Copilot Prompt Template: Resolve Missing Elements, Tags, and Columns for Greenova POC](#github-copilot-prompt-template-resolve-missing-elements-tags-and-columns-for-greenova-poc)
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
Prompt for resolving missing elements, tags, and columns in files, templates, and database to ensure the Greenova proof of concept (POC) fully supports all required CRUD and navigation features.
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

# GitHub Copilot Prompt Template: Resolve Missing Elements, Tags, and Columns for Greenova POC

## Goal

Ensure the Greenova proof of concept (POC) fully supports:
- User login
- Project creation and environmental mechanism definition
- Adding obligations to projects
- Assigning responsibilities to users
- Monitoring compliance status
- CRUD for user profiles and company information
- Drill-down navigation: mechanisms → procedures → obligations
- CRUD for obligations (including overdue obligations)
- Tooltip on overdue obligations card listing clickable, detailed overdue obligations
- Editing obligations from detail pages
- All CRUD operations for overdue obligations

## Context

- Many files, templates, and database models are missing required elements, tags, or columns, preventing the POC from working as intended.
- The following features must be implemented and working:
  1. Log in using credentials created during setup
  2. Create projects and define environmental mechanisms
  3. Add obligations related to projects
  4. Assign responsibilities to users
  5. Monitor compliance status
  6. CRUD user profiles and company information
  7. Drill down into mechanisms, then procedures, then obligations for details
  8. Perform CRUD on obligations
  9. Tooltip on overdue obligations card lists clickable overdue obligations, linking to detail pages
  10. Edit obligations from detail pages
  11. Full CRUD for overdue obligations
- See these issues/PRs for more details and requirements:
  - https://github.com/enveng-group/dev_greenova/pull/171
  - https://github.com/enveng-group/dev_greenova/issues/160
  - https://github.com/enveng-group/dev_greenova/issues/158
  - https://github.com/enveng-group/dev_greenova/issues/159
  - https://github.com/enveng-group/dev_greenova/issues/163
  - https://github.com/enveng-group/dev_greenova/issues/156
  - https://github.com/enveng-group/dev_greenova/issues/161
  - https://github.com/enveng-group/dev_greenova/issues/162
  - https://github.com/enveng-group/dev_greenova/pull/174

## Objectives

- Identify and add all missing elements, tags, and columns in files, templates, and database models required for the above features.
- Ensure all CRUD operations and navigation paths are present and functional.
- Implement tooltips and clickable lists for overdue obligations as described.
- Ensure all templates and forms have the necessary fields, blocks, and logic.
- Update database models and migrations to include missing columns/relations.
- Reference and resolve all requirements from the linked issues/PRs.
- Iterate using all available MCP servers (github, fetch, sequential-thinking, filesystem, context7) to:
  - Analyze code, templates, and database schema
  - Plan and execute necessary changes
  - Validate with pre-commit and tests after each change
- Document all changes and ensure compliance with project standards.

## Sources

- All relevant Django models, forms, views, templates, and static files in the workspace
- Database migration files
- The above GitHub issues and PRs
- Project documentation and standards (context7)

## Expectations

- Use all available MCP servers to:
  - Analyze and fix missing elements, tags, and columns
  - Implement and validate all required CRUD and navigation features
  - Update code, templates, and database as needed
  - Run pre-commit and tests after each change
  - Iterate until all requirements are met and all checks pass
- Ensure all changes align with project coding, documentation, and testing standards

## Acceptance Criteria

- All required elements, tags, and columns are present in files, templates, and database
- All CRUD and navigation features described above are implemented and working
- Overdue obligations tooltip lists clickable obligations linking to detail pages
- Obligations can be edited from their detail pages
- All pre-commit checks and tests pass
- All changes are documented as per project standards

## Instructions

- Use this prompt to guide Copilot in resolving the described missing elements/tags/columns issue
- Reference all relevant files, issues, and documentation
- Use github, fetch, sequential-thinking, filesystem, and context7 for planning and execution
- Iterate until the POC works as described and all checks pass

## Additional Guidelines

- Always use the simplest effective solution
- Follow the project's coding, documentation, and testing standards (see context7)
- Document any changes or decisions clearly in code and commit messages
- Use semantic reasoning and all available MCP servers for planning and execution
