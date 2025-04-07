# GitHub Issue Creation Template for Greenova

This template provides standardized commands for creating GitHub issues from
bug reports using the GitHub CLI.

# GitHub Issue Creation Template for Greenova

This template provides standardized commands for creating GitHub issues from
bug reports using the GitHub CLI.

## Basic Issue Creation Command

## Basic Issue Creation Command

`````fish
# Basic structure of the gh issue create command
````fish
# Basic structure of the gh issue create command
set repo "https://github.com/enveng-group/dev_greenova"
set title "bug: Obligation form has mandatory recurring field and"\
" inability to customize obligation numbers"
set body "
## Description

Users are experiencing two issues with the Obligation registration form:
(1) the \"recurring obligation\" checkbox is required even for non-recurring
obligations, and (2) users cannot customize obligation numbers to use specific
formats like \"W6875 Condition 1.6a\" instead of the auto-generated
\"PCEMP-237\" format.

## Current Behavior

1. The \"recurring obligation\" checkbox is mandatory, forcing users to
   incorrectly mark non-recurring obligations as recurring
2. Obligation numbers are auto-generated in the \"PCEMP-XXX\" format and cannot
   be customized

## Expected Behavior

1. The \"recurring obligation\" checkbox should be optional, allowing users to
   submit the form without checking it
2. Users should be able to customize obligation numbers to match specific
   formats like \"W6875 Condition 1.6a\"

## Steps to Reproduce

1. Log into the Greenova application
2. Navigate to the Obligation registration form
3. Attempt to create a new obligation
4. Try to leave the \"recurring obligation\" checkbox unchecked
5. Notice that the form cannot be submitted without checking this box
6. Also observe that the obligation number field cannot be edited to use custom
   formats like \"W6875 Condition 1.6a\"

## Environment Details

- **Application Version**: Latest production deployment of Greenova
  environmental management system
- **Operating System**: Various (issue is application-specific, not OS-dependent)
- **Browser**: Various (issue is server-side, not browser-specific)
- **Device**: Desktop/Laptop

## Technical Context

- **Django Version**: 4.1.13
- **Python Version**: 3.9.21
- **Affected Module/App**: obligations
- **Frontend Technologies**: PicoCSS, django-hyperscript, django-htmx
- **Database**: SQLite3 (development)
- **Affected Files**:
  - `/workspaces/greenova/greenova/obligations/forms.py` (ObligationForm)
  - `/workspaces/greenova/greenova/obligations/models.py` (Obligation model)

## Error Details

```
No explicit error messages, but form validation prevents submission when the
recurring obligation checkbox is unchecked.
```

## Impact Assessment

- **Severity**: Medium
- **Frequency**: 100% (Affects every creation of an obligation)
- **User Impact**: Data integrity issues as non-recurring obligations are
incorrectly marked as recurring. Difficulty in navigating and identifying
specific obligations due to inability to use custom obligation numbers.
Reduced usability of the environmental obligations register for projects where
specific numbering formats are required by regulatory documents.

## Proposed Implementation

1. In `ObligationForm` class (`obligations/forms.py`), modify the
`recurring_obligation` field definition to set `required=False`
2. Update the `Obligation` model and form to allow custom obligation numbers:
   - Modify validation in models.py to accept alternative formats beyond PCEMP-XXX
   - Update the form to make the obligation_number field editable for new obligations
   - Add a configuration option to toggle between auto-generated and custom
   obligation numbering

## Acceptance Criteria

- [ ] Users can save obligations without checking the recurring obligation checkbox
- [ ] Users can enter custom obligation numbers in formats like
\"W6875 Condition 1.6a\"
- [ ] Existing functionality for auto-generating obligation numbers is
preserved when needed
- [ ] Form validation still ensures obligation numbers are unique
- [ ] Tests are updated to verify these fixes
- [ ] Documentation is updated to reflect the changes in behavior

## Additional Context

- This issue affects users working with the primary environmental
mechanism 'W6875/2023/1' who need to reference specific conditions like
\"Condition 1.2\", \"Condition 1.2a\", etc.
- User is currently adding obligations under this mechanism with incorrect
numbering (PCEMP-237 instead of the desired W6875 Condition 1.6a)
- Users have provided feedback that they cannot currently navigate and maintain
 the environmental obligation register effectively without these changes
"

# Execute the command to create the issue
## Adding Labels

After creating the issue, add appropriate labels based on the issue
characteristics:

```fish
# Get the issue number from the created issue
set issue_number [ISSUE_NUMBER]

# Add appropriate labels
gh issue edit $issue_number --add-label "bug,ui,forms,help wanted"

# Add component-specific labels as needed
gh issue edit $issue_number --add-label "django"

# Add priority label based on severity
gh issue edit $issue_number --add-label "priority-medium"
```

## Creating New Labels (if needed)

If a new label is needed:

```fish
gh label create "label-name" --description "Description of the label" --color "#HEX_COLOR"
```

## Common Label Colors

- Bug: #d73a4a (red)
- Enhancement: #a2eeef (light blue)
- Documentation: #0075ca (blue)
- Good first issue: #7057ff (purple)
- Help wanted: #008672 (green)
- Priority High: #ff0000 (bright red)
- Priority Medium: #ff8c00 (orange)
- Priority Low: #ffff00 (yellow)

## Example Complete Issue Creation

```fish
## Example Complete Issue Creation
set title "bug: Obligation form has mandatory recurring field and"\
" inability to customize obligation numbers"
set body "
## Description

Users are experiencing two issues with the Obligation registration form:
(1) the \"recurring obligation\" checkbox is required even for non-recurring
obligations, and (2) users cannot customize obligation numbers to use specific
formats like \"W6875 Condition 1.6a\" instead of the auto-generated
\"PCEMP-237\" format.

## Current Behavior

1. The \"recurring obligation\" checkbox is mandatory, forcing users to
incorrectly mark non-recurring obligations as recurring
2. Obligation numbers are auto-generated in the \"PCEMP-XXX\" format and
cannot be customized

## Expected Behavior

1. The \"recurring obligation\" checkbox should be optional, allowing users to
submit the form without checking it
2. Users should be able to customize obligation numbers to match specific
formats like \"W6875 Condition 1.6a\"

## Steps to Reproduce

1. Log into the Greenova application
2. Navigate to the Obligation registration form
3. Attempt to create a new obligation
4. Try to leave the \"recurring obligation\" checkbox unchecked
5. Notice that the form cannot be submitted without checking this box
6. Also observe that the obligation number field cannot be edited to use custom
 formats like \"W6875 Condition 1.6a\"

## Environment Details

- **Application Version**: Latest production deployment of Greenova
environmental management system
- **Operating System**: Various (issue is application-specific, not OS-dependent)
- **Browser**: Various (issue is server-side, not browser-specific)
- **Device**: Desktop/Laptop

## Technical Context

- **Django Version**: 4.1.13
- **Python Version**: 3.9.21
- **Affected Module/App**: obligations
- **Frontend Technologies**: PicoCSS, django-hyperscript, django-htmx
- **Database**: SQLite3 (development)
- **Affected Files**:
  - `/workspaces/greenova/greenova/obligations/forms.py` (ObligationForm)
  - `/workspaces/greenova/greenova/obligations/models.py` (Obligation model)

## Impact Assessment

- **Severity**: Medium
- **Frequency**: 100% (Affects every creation of an obligation)
- **User Impact**:
  - Data integrity issues as non-recurring obligations are incorrectly marked
  as recurring
  - Difficulty in navigating and identifying specific obligations
  - Reduced usability of the environmental obligations register where specific
  numbering formats are required by regulatory documents

## Proposed Implementation

1. In `ObligationForm` class (`obligations/forms.py`), modify the
`recurring_obligation` field definition to set `required=False`
2. Update the `Obligation` model and form to allow custom obligation numbers:
   - Modify validation in models.py to accept alternative formats beyond PCEMP-XXX
   - Update the form to make the obligation_number field editable for new obligations
   - Add a configuration option to toggle between auto-generated and custom
   obligation numbering

## Acceptance Criteria

- [ ] Users can save obligations without checking the recurring obligation checkbox
- [ ] Users can enter custom obligation numbers in formats
like \"W6875 Condition 1.6a\"
- [ ] Existing functionality for auto-generating obligation numbers is
preserved when needed
- [ ] Form validation still ensures obligation numbers are unique
- [ ] Tests are updated to verify these fixes
- [ ] Documentation is updated to reflect the changes in behavior

## Additional Context

This issue affects users working with the primary environmental mechanism
'W6875/2023/1' who need to reference specific conditions like
\"Condition 1.2\", \"Condition 1.2a\", etc. User is currently adding
obligations under this mechanism with incorrect numbering (PCEMP-237
instead of the desired W6875 Condition 1.6a).
"

gh issue create --repo $repo --title $title --body $body

# After creating, add appropriate labels
gh issue edit [ISSUE_NUMBER] --add-label "bug,ui,forms,django,priority-medium,
help wanted"
```
`````
