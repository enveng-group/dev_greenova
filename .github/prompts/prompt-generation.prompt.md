---
description:
  Template for generating automated issue resolution prompts for Copilot,
  including context, objectives, and acceptance criteria.
mode: agent

tools:
  - filesystem
  - dbcode
  - context7
  - json
  - git
  - sequential-thinking
  - github
---

<!-- filepath: /workspaces/greenova/.github/prompts/promp-generation.prompt.md -->

# GitHub Copilot Prompt Template for Automated Issue Resolution

## Goal

Describe the main goal or problem to be solved. Be concise and specific.

## Context

Provide relevant background information, including system, environment, or
business context. Include any error messages, stack traces, or logs if
applicable.

## Objectives

List the specific objectives or outcomes you expect from Copilot. Use bullet
points for clarity.

## Sources

- List relevant files in the workspace (relative paths):
  - e.g., `src/app/models.py`
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
