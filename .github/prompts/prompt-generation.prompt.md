<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [GitHub Copilot Prompt Template for Automated Issue Resolution](#github-copilot-prompt-template-for-automated-issue-resolution)
  - [Goal](#goal)
  - [Context](#context)
  - [Objectives](#objectives)
  - [Sources](#sources)
  - [Expectations](#expectations)
  - [Acceptance Criteria](#acceptance-criteria)
  - [Instructions](#instructions)
  - [Additional Guidelines](#additional-guidelines)
  - [Frontend Technologies](#frontend-technologies)
    - [Technology Priority Order (Expanded)](#technology-priority-order-expanded)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

---

description:
Template for generating automated issue resolution prompts for Copilot,
including context, objectives, and acceptance criteria.
mode: agent

tools:
<<<<<<< HEAD
  - filesystem
  - dbcode
  - context7
  - json
  - git
  - sequential-thinking
  - github
||||||| parent of 37e6b25 (Squashed commit of the following:)
  - filesystem
  - semantic_search
  - get_errors
  - run_tests
  - file_search
  - read_file
  - insert_edit_into_file
  - context7
  - json
  - git
  - sequential-thinking
=======

- context7 # REQUIRED: Use for all context and background information
- json
- git
- fetch # REQUIRED: Use for all web content retrieval (e.g., documentation, reports)
- filesystem # REQUIRED: Use for all file reading, writing, and editing
- sequential-thinking # REQUIRED: Use for all planning, reasoning, and stepwise logic
- github

>>>>>>> 37e6b25 (Squashed commit of the following:)
---

<!-- filepath: /workspaces/greenova/.github/prompts/promp-generation.prompt.md -->

# GitHub Copilot Prompt Template for Automated Issue Resolution

## Goal

Describe the main goal or problem to be solved. Be concise and specific.

## Context

Provide relevant background information, including system, environment, or
business context. Include any error messages, stack traces, or logs if
applicable.

- **All code, models, and CRUD logic must be structured according to the actual database schema in `schema.json` and sample data in `data.json`. Use these files as the authoritative source for field names, types, relationships, and data structure.**
- \*\*All templates must use Django Template Language (DTL) with `.html` extension.

## Objectives

List the specific objectives or outcomes you expect from Copilot. Use bullet
points for clarity.

## Sources

- List relevant files in the workspace (relative paths):

  - e.g., `src/app/models.py`
  - e.g., `templates/app/example.html`

- List relevant GitHub repositories and branches:
  - e.g., `https://github.com/org/repo/tree/branch`
- List URLs to documentation/manuals/reference material:
  - e.g., `https://docs.djangoproject.com/en/5.2/`

## Expectations

Describe what you expect Copilot to do (e.g., iterate using all available MCP
servers, refactor code, update documentation, run pre-commit checks, etc.).

## Acceptance Criteria

- List clear, testable criteria for completion (e.g., all pre-commit checks
  pass, error is resolved, code is documented, etc.)

## Instructions

- Paste the error or issue description below this prompt.
- Include this prompt file in your Copilot chat session.
- Click submit for Copilot to utilize all available MCP servers and iterate
  until the issue is resolved.

## Additional Guidelines

- **Documentation Lookup**: Always use the `fetch` and `context7` MCP servers
  to look up and reference official documentation for the following
  technologies as needed:

  - [GSAP Animation](https://gsap.com/docs/v3/)
<<<<<<< HEAD
  - [PicoCSS Classless](https://picocss.com/docs/classless)
  - [Hyperscript](https://hyperscript.org/docs/)
  - [TypeScript](https://www.typescriptlang.org/docs/)
  - [HTMX](https://htmx.org/docs/)
  - [django-hyperscript](https://github.com/LucLor06/django-hyperscript#readme)
  - [django-htmx](https://django-htmx.readthedocs.io/en/latest/)
  - [AssemblyScript](https://www.assemblyscript.org/introduction.html)
  - [Django](https://docs.djangoproject.com/en/5.2/)
  - [Protobuf3](https://protobuf.dev/)
  - [SQLite](https://www.sqlite.org/docs.html)
  - [django-pb-model](https://pypi.org/project/django-pb-model/)
  - [Matplotlib](https://matplotlib.org/stable/users/index)
  - [django_matplotlib](https://github.com/scidam/django_matplotlib)
  - [Plotly](https://plotly.com/python/)
  - [Pandas](https://pandas.pydata.org/docs/)
  - [NumPy](https://numpy.org/doc/stable/user/index.html#user)
  - [django-csp](https://django-csp.readthedocs.io/en/latest/)
  - [django-template-partials](https://github.com/carltongibson/django-template-partials?tab=readme-ov-file#basic-usage)
  - [dj-all-auth](https://github.com/deviserops/dj-all-auth)
  - [python-dotenv-vault](https://github.com/dotenv-org/python-dotenv-vault)

- **Semantic Reasoning**: Use the `semantic-thinking` MCP server for all
  reasoning, planning, and stepwise solution development.

1. **Restructured Text (RST)**: Use as the foundational layer for body,
   content, and messages for HTML.
2. **HTML**: Utilize for semantic structure and markup. Do not apply inline
   styles and scripts.
3. **Protobuf3**: Primary implementation for data serialization.
4. **Classless-CSS**: Apply minimal styling using Classless-PicoCSS as HTML.
5. **django-hyperscript**: Primary implementation for client-side interactions.
6. **django-htmx**: Secondary implementation for client-side interactions only
   to complement django-hyperscript.
7. **SASS/PostCSS**: Use for advanced styling needs when required.
8. **TypeScript**: Introduce only when django-hyperscript and django-htmx
   cannot meet the requirements. Use TypeScript for complex logic. Avoid using
   TypeScript for simple interactions that can be handled by django-hyperscript
   or django-htmx.
9. **AssemblyScript**: Primary implementation for critical client-side
   interactions and web assembly (WASM) implementations.
||||||| parent of 37e6b25 (Squashed commit of the following:)
1. **Restructured Text (RST)**: Use as the foundational layer for body,
   content, and messages for HTML.
2. **HTML**: Utilize for semantic structure and markup. Do not apply inline
   styles and scripts.
3. **Protobuf3**: Primary implementation for data serialization.
4. **Classless-CSS**: Apply minimal styling using Classless-PicoCSS as HTML.
5. **django-hyperscript**: Primary implementation for client-side interactions.
6. **django-htmx**: Secondary implementation for client-side interactions only
   to complement django-hyperscript.
7. **SASS/PostCSS**: Use for advanced styling needs when required.
8. **TypeScript**: Introduce only when django-hyperscript and django-htmx
   cannot meet the requirements. Use TypeScript for complex logic. Avoid using
   TypeScript for simple interactions that can be handled by django-hyperscript
   or django-htmx.
9. **AssemblyScript**: Primary implementation for critical client-side
   interactions and web assembly (WASM) implementations.
=======
  - [Hyperscript](https://hyperscript.org/docs/)
  - [TypeScript](https://www.typescriptlang.org/docs/)
  - [HTMX](https://htmx.org/docs/)
  - [django-hyperscript](https://github.com/LucLor06/django-hyperscript#readme)
  - [django-htmx](https://django-htmx.readthedocs.io/en/latest/)
  - [AssemblyScript](https://www.assemblyscript.org/introduction.html)
  - [Django](https://docs.djangoproject.com/en/5.2/)
  - [Protobuf3](https://protobuf.dev/)
  - [SQLite](https://www.sqlite.org/docs.html)
  - [django-pb-model](https://pypi.org/project/django-pb-model/)
  - [Matplotlib](https://matplotlib.org/stable/users/index)
  - [django_matplotlib](https://github.com/scidam/django_matplotlib)
  - [Plotly](https://plotly.com/python/)
  - [Pandas](https://pandas.pydata.org/docs/)
  - [NumPy](https://numpy.org/doc/stable/user/index.html#user)
  - [django-csp](https://django-csp.readthedocs.io/en/latest/)
  - [dj-all-auth](https://github.com/deviserops/dj-all-auth)
  - [python-dotenv-vault](https://github.com/dotenv-org/python-dotenv-vault)

- **Semantic Reasoning**: Use the `semantic-thinking` MCP server for all
  reasoning, planning, and stepwise solution development.

## Frontend Technologies

- **Simplicity First**: Always choose the simplest effective solution
- **Plain Text / HTML First**: Start with semantic HTML before adding
  complexity

### Technology Priority Order (Expanded)

1. **Restructured Text (RST)**: Use for documentation, content, and messages. Prefer for all technical docs and user-facing help.
2. **Django Template Language (DTL)**: Use for semantic structure. All templates must use `.html` extension and be compatible with Django's built-in template engine. No inline styles/scripts. All templates must be accessible and pass djlint.
3. **Protobuf3**: Use for all data serialization between backend and frontend. Prefer over JSON for APIs and data exports.
4. **django-bootstrap5**: Use as the sole primary styling framework for all new development.
5. **django-hyperscript**: Use for all simple client-side interactions. Avoid custom JS unless required.
6. **django-htmx**: Use for AJAX, partial updates, and dynamic content loading. Only when django-hyperscript is insufficient.
7. **scss**: Use for advanced styling and theming, in conjunction with django-bootstrap5. Only after exhausting bootstrap utility options.
8. **AssemblyScript**: Use exclusively for all client-side interactivity logic that cannot be solved by django-hyperscript or django-htmx. Do not use JavaScript in this project.
>>>>>>> 37e6b25 (Squashed commit of the following:)
