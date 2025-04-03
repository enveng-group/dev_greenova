# GitHub Issue Creation Template for Greenova

This template provides standardized commands for creating GitHub issues from
bug reports using the GitHub CLI.

## Basic Issue Creation Command

````fish
# Basic structure of the gh issue create command
set repo "https://github.com/enveng-group/dev_greenova"
set title "bug: Brief description of the issue"
set body "
## Description

[Copy summary from bug report]

## Current Behavior

[Copy actual result and any error messages from bug report]

## Expected Behavior

[Copy expected result from bug report]

## Steps to Reproduce

[Copy numbered steps from bug report]

## Environment Details

- **Application Version**: [From bug report]
- **Operating System**: [From bug report]
- **Browser**: [From bug report, if applicable]
- **Device**: [From bug report]

## Technical Context

- **Django Version**: 4.1.13
- **Python Version**: 3.9.21
- **Affected Module/App**: [Identify affected component]
- **Frontend Technologies**: PicoCSS, django-hyperscript, django-htmx

## Error Details

#```html

[Insert relevant error message or traceback summary]

#```

For complete traceback, see original bug report.

## Impact Assessment

- **Severity**: [Critical/High/Medium/Low, from bug report]
- **Frequency**: [How often issue occurs, from bug report]
- **User Impact**: [Description from bug report]

## Proposed Implementation

[Outline potential fix approach based on bug analysis]

## Acceptance Criteria

- [ ] Issue is resolved with no regressions
- [ ] Documentation is updated if necessary
- [ ] Tests are added/updated to cover the fix
- [ ] [Additional criteria specific to this issue]

## Additional Context

[Any workarounds, related issues, or other relevant information from bug report]
"

# Execute the command to create the issue
gh issue create --repo $repo --title $title --body $body
````

## Adding Labels

After creating the issue, add appropriate labels based on the issue
characteristics:

```fish
# Get the issue number from the created issue
set issue_number [ISSUE_NUMBER]

# Add appropriate labels
gh issue edit $issue_number --add-label "bug,help wanted"

# Add component-specific labels as needed
gh issue edit $issue_number --add-label "django,database"

# Add priority label based on severity
gh issue edit $issue_number --add-label "priority-high"
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
set repo "https://github.com/enveng-group/dev_greenova"
set title "bug: Dashboard fails to load environmental metrics when filtering by project"
set body "
## Description

When applying the project filter on the dashboard, environmental metrics don't update and the page shows a loading spinner indefinitely.

## Current Behavior

The loading spinner appears and never stops, metrics don't update after selecting a project filter and clicking 'Apply Filter'.

## Expected Behavior

The dashboard should refresh and show metrics specific to the selected project.

## Steps to Reproduce

1. Log in to Greenova using a standard user account
2. Navigate to \"Dashboard\" from the main menu
3. Click the \"Filter\" button in the top right corner
4. Select \"Project A\" from the dropdown list
5. Click \"Apply Filter\"

## Environment Details

- **Application Version**: 1.5.2
- **Operating System**: Windows 11
- **Browser**: Chrome 120.0.6099.217
- **Device**: Dell XPS 15 laptop

## Technical Context

- **Django Version**: 4.1.13
- **Python Version**: 3.9.21
- **Affected Module/App**: dashboard
- **Frontend Technologies**: PicoCSS, django-hyperscript, django-htmx

## Error Details

Console error:
```

GET https://greenova.example.com/api/dashboard/metrics?project_id=42 500
(Internal Server Error)

```

Network tab shows the request fails with a 500 error.

## Impact Assessment

- **Severity**: High
- **Frequency**: Always (100% of attempts)
- **User Impact**: Users cannot view project-specific metrics, affecting compliance monitoring and reporting capabilities

## Proposed Implementation

- Investigate the API endpoint handler for dashboard metrics
- Check for proper error handling when filtering by project
- Verify database queries are correctly formed with project filters
- Add appropriate error messaging if project data is unavailable

## Acceptance Criteria

- [ ] Dashboard loads and displays metrics correctly when filtering by project
- [ ] Error handling is improved to provide meaningful feedback on failures
- [ ] Tests are added to verify filtering functionality
- [ ] Performance is maintained with large datasets

## Additional Context

Refreshing the page and trying again doesn't resolve the issue. The problem started after the recent dashboard filter feature was added in version 1.5.0.
"

gh issue create --repo $repo --title $title --body $body

# After creating, add appropriate labels
gh issue edit [ISSUE_NUMBER] --add-label "bug,dashboard,api,help wanted,priority-high"
```
