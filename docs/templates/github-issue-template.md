# GitHub Issue Creation Template for Greenova

This template provides standardized commands for creating GitHub issues from
bug reports using the GitHub CLI.

## Basic Issue Creation Command

```fish
# Basic structure of the gh issue create command
set repo "https://github.com/enveng-group/dev_greenova"
set title "enhancement: Modify responsibility table to use text input instead of dropdown"
set body "
## Description

The responsibility table needs modification to replace the dropdown of constant values in the /admin/ view with a text box that allows administrators to create new responsibility values as strings. This change is needed to support a future use case where notifications (emails) will be triggered based on the responsibility (role) assigned to users.

## Current Behavior

Currently, when adding a responsibility in the admin interface, administrators are limited to selecting from a predefined list of constants in a dropdown menu. This restricts the ability to create custom responsibilities that might be needed for specific notification workflows.

## Expected Behavior

- Replace the dropdown selector in the responsibility admin interface with a text input field
- Allow administrators to enter any string value as a new responsibility
- Store these custom responsibility values appropriately in the database
- Ensure backward compatibility with existing responsibility assignments
- Lay groundwork for a future notification system that will send emails to users based on their assigned responsibilities

## Technical Context

- **Django Version**: 4.1.13
- **Python Version**: 3.9.21
- **Frontend Technologies**: PicoCSS, django-hyperscript, django-htmx
- **Database**: SQLite3 (development)
- **Affected Module/App**: Responsibility app
- **Affected Files**:
  - responsibility/models.py
  - responsibility/admin.py
  - responsibility/forms.py (may need to be created)
  - core/utils/roles.py (likely referenced for current constants)
- **Template Engine**: Django Template Language

## Impact Assessment

- **Severity**: Medium
- **User Impact**: Administrators will have more flexibility in assigning responsibilities
- **Frequency**: Will affect all administrative operations involving responsibility assignments

## Proposed Implementation

1. Modify the Responsibility model to allow free-text input:
   - Ensure the name field doesn't have any choice constraints
   - Add any necessary validation for the text input

2. Update the admin interface:
   - Modify ResponsibilityAdmin class to use a TextInput widget instead of a dropdown
   - Add appropriate form validation

3. Update any utility functions in core/utils/roles.py:
   - Ensure get_responsibility_choices() and similar functions work with dynamic values
   - May need to modify to fetch from database rather than using constants

4. Add migration to preserve existing responsibility values:
   - Ensure current responsibility assignments are preserved
   - Handle any data migration needed for the transition

5. Add documentation:
   - Document how to use the new text input feature
   - Document future plans for notification system

## Acceptance Criteria

- [ ] Responsibility admin interface displays a text input instead of a dropdown
- [ ] Administrators can create new responsibilities by entering any string value
- [ ] Existing responsibilities are preserved and remain functional
- [ ] All views and forms that reference responsibilities continue to work
- [ ] All unit tests pass with the new implementation
- [ ] Code is properly documented
- [ ] Migration safely handles existing data

## Labels

- responsibility
- priority-high
- enhancement
- admin
- database
- refactoring
- future-proofing"

# Execute the command to create the issue
gh issue create --repo $repo --title $title --body $body --label "responsibility,priority-high,enhancement,admin,database,refactoring,future-proofing"
```
