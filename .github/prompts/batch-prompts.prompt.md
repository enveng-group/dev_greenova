---
description:
  Batch of sequential micro-prompts for Copilot agent to resolve critical code
  quality issues in the Greenova project, following the template and standards
  in prompt-generation.prompt.md.
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

# Batch Micro-Prompts for Critical Issue Resolution

---

## Micro-Prompt 1: Add Missing/Incomplete Docstrings

### Goal

Add missing or incomplete Google-style docstrings to all modules, classes,
methods, and packages as required by project standards and flagged by ruff
(D100–D107, D104, D105, D106, D107).

### Context

Many modules, classes, and methods lack required docstrings, impacting
readability, maintainability, and compliance.

### Objectives

- Add or complete Google-style docstrings for all flagged code elements.
- Ensure docstrings meet formatting and content requirements.

### Acceptance Criteria

- All D100–D107, D104, D105, D106, D107 ruff errors are resolved.
- All code elements have appropriate Google-style docstrings.

---

## Micro-Prompt 2: Annotate Mutable Class Attributes with ClassVar

### Goal

Annotate all mutable class attributes (e.g., lists, dicts) in Django model and
form classes with typing.ClassVar, as required by ruff (RUF012) and project
standards.

### Context

Unannotated mutable class attributes can cause bugs and type-checking issues.

### Objectives

- Identify all mutable class attributes in relevant classes.
- Annotate them with typing.ClassVar.

### Acceptance Criteria

- All RUF012 ruff errors are resolved.
- All mutable class attributes are properly annotated.

---

## Micro-Prompt 3: Fix Lines Exceeding 88 Characters

### Goal

Refactor all lines exceeding 88 characters to comply with PEP 8 and project
standards (E501).

### Context

Long lines reduce readability and violate style guidelines.

### Objectives

- Break long lines using implicit line continuation or string concatenation.
- Ensure code remains readable and functional.

### Acceptance Criteria

- All E501 ruff errors are resolved.
- No lines exceed 88 characters.

---

## Micro-Prompt 4: Correct Function Naming Conventions

### Goal

Rename methods/functions that violate PEP 8 snake_case naming conventions
(N802).

### Context

Some methods (e.g., SerializeToString, ParseFromString) use incorrect naming.

### Objectives

- Identify all functions/methods with incorrect naming.
- Rename them to snake_case.

### Acceptance Criteria

- All N802 ruff errors are resolved.
- All functions/methods use snake_case.

---

## Micro-Prompt 5: Replace Bare Except Clauses

### Goal

Replace all bare except: clauses with specific exception handling to improve
code safety and quality (E722).

### Context

Bare except can mask unexpected errors and is a security/code quality risk.

### Objectives

- Identify all bare except: clauses.
- Replace with except Exception: or more specific exceptions as appropriate.

### Acceptance Criteria

- All E722 ruff errors are resolved.
- No bare except: clauses remain.

---

## Micro-Prompt 6: Fix Docstring Formatting (D205)

### Goal

Ensure all docstrings have a blank line between the summary and description, as
required by ruff (D205) and project standards.

### Context

Some docstrings are missing the required blank line, affecting readability and
compliance.

### Objectives

- Review all docstrings for formatting.
- Add blank lines where required.

### Acceptance Criteria

- All D205 ruff errors are resolved.
- All docstrings have correct formatting.

---
