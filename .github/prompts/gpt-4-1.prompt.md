<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Fix Import Ordering Issues - Micro Prompt 1](#fix-import-ordering-issues---micro-prompt-1)
  - [Goal](#goal)
  - [Context](#context)
  - [Objectives](#objectives)
  - [Sources](#sources)
  - [Expectations](#expectations)
  - [Acceptance Criteria](#acceptance-criteria)
  - [Instructions](#instructions)
    - [Step 1: Environment Setup](#step-1-environment-setup)
    - [Step 2: Identify Problem Files](#step-2-identify-problem-files)
    - [Step 3: Fix Import Structure](#step-3-fix-import-structure)
    - [Step 4: Priority Files to Fix](#step-4-priority-files-to-fix)
    - [Step 5: Validate Changes](#step-5-validate-changes)
    - [Step 6: Iterate Until Clean](#step-6-iterate-until-clean)
  - [Additional Guidelines](#additional-guidelines)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

---

description:
This micro-prompt focuses specifically on resolving import ordering issues in the Greenova Django project. It addresses E402, F404, and PLC0415 errors by ensuring all imports are moved to the top of files and follow proper ordering conventions. This is the first in a series of sequential micro-prompts for code quality improvements.

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

# Fix Import Ordering Issues - Micro Prompt 1

## Goal

Resolve all import ordering and placement issues in the Greenova Django project by moving imports to the top of files and fixing E402, F404, and PLC0415 linting errors.

## Context

The ruff linter reports import ordering violations throughout the codebase. These errors prevent pre-commit hooks from passing and violate project coding standards. All imports must be moved to the top of each Python file and follow the proper ordering structure defined in the project guidelines.

Common error patterns:

- E402: module level import not at top of file
- F404: future import(s) not at top of file
- PLC0415: import should be placed at the top of the module

## Objectives

- Identify all Python files with import ordering violations
- Move all imports to the top of each file following proper structure
- Maintain existing import functionality while fixing placement
- Ensure pre-commit hooks pass for import-related checks
- Preserve code functionality while improving compliance

## Sources

- All Python files in the greenova project directory
- Project coding standards from context7
- Ruff linter output for E402, F404, PLC0415 errors
- Import structure guidelines from project documentation

## Expectations

- All imports moved to top of files in correct order
- No breaking changes to existing functionality
- All import-related linting errors resolved
- Pre-commit hooks pass for ruff-check and isort
- Code follows project import structure standards

## Acceptance Criteria

- Zero E402, F404, and PLC0415 errors when running `ruff check --select=E402,F404,PLC0415 .`
- All pre-commit import checks pass: `pre-commit run ruff-check` and `pre-commit run isort`
- Application functionality remains intact after changes
- Import structure follows project guidelines (future, standard, third-party, local)
- No circular import issues introduced

## Instructions

### Step 1: Environment Setup

```bash
source .venv/bin/activate
```

### Step 2: Identify Problem Files

```bash
ruff check --select=E402,F404,PLC0415 . --output-format=text
```

### Step 3: Fix Import Structure

For each flagged file, reorganize imports following this exact pattern:

```python
# Future imports (if any)
from __future__ import annotations

# Standard library imports
import os
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

# Third-party imports
import django
from django.contrib import admin
from django.db import models

# Local application imports
from core.models import BaseModel
from utilities.helpers import format_date
```

### Step 4: Priority Files to Fix

Focus on these common Django files:

- `greenova/*/models.py`
- `greenova/*/views.py`
- `greenova/*/admin.py`
- `greenova/*/forms.py`
- `greenova/*/urls.py`
- `greenova/*/apps.py`
- `greenova/landing/commons.py`
- `greenova/landing/constants.py`
- `greenova/landing/context_processors.py`
- `greenova/landing/middleware.py`
- `greenova/landing/mixins.py`
- `greenova/landing/permissions.py`
- `greenova/landing/signals.py`
- `greenova/landing/tasks.py`
- `greenova/landing/validators.py`
- `greenova/landing/templatetags/landing_tags.py`

### Step 5: Validate Changes

```bash
git add .
pre-commit run ruff-check
pre-commit run isort
```

### Step 6: Iterate Until Clean

Repeat steps 2-5 until all import ordering errors are resolved.

## Additional Guidelines

- **Preserve Functionality**: Only move imports, do not modify import names or aliases
- **Maintain Grouping**: Keep logical import groups but ensure proper placement
- **No Circular Imports**: Verify no circular import issues are introduced
- **Use Filesystem MCP**: All file operations must use the filesystem MCP server
- **Use Sequential Thinking**: Plan each file change using the sequential-thinking MCP server

**Next Step**: After successfully completing this micro-prompt with zero import ordering errors, proceed to **gpt-4-2.prompt.md** for adding missing copyright notices and removing commented-out code.
