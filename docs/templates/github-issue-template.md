# gh issue create template for Greenova Repository

```fish

set repo "https://github.com/enveng-group/dev_greenova"
set title "Bug: Fix OperationalError in ProjectMembership Add View"
set body "
## Description

An \`OperationalError\` occurs when attempting to access the \`ProjectMembership\` add view in the Django admin interface. The error indicates that the column \`projects_project.company_id\` does not exist in the database.

## Current Behavior

- Accessing the URL \`/admin/projects/projectmembership/add/\` results in the following error:
  \`\`\`
  Exception Type: OperationalError
  Exception Value: no such column: projects_project.company_id
  \`\`\`

- The error occurs in the template \`fieldset.html\` at line 19 while rendering the form field.

## Expected Behavior

- The \`ProjectMembership\` add view should render without errors, allowing users to add project memberships via the Django admin interface.

## Steps to Reproduce

1. Navigate to the Django admin interface.
2. Go to the \`ProjectMembership\` model under the \`projects\` app.
3. Click on the \`Add\` button.
4. Observe the error.

## Technical Context

- **Django Version**: 4.1.13
- **Python Version**: 3.9.21
- **Affected Module/App**: \`projects\`
- **Template**: \`fieldset.html\`

## Proposed Implementation

- Verify the database schema to ensure the \`company_id\` column exists in the \`projects_project\` table.
- If the column is missing, update the database schema using a Django migration.
- Review the model definition for \`projects_project\` to ensure the \`company\` field is correctly defined.
- Update the admin form or view logic if necessary to handle the missing column gracefully.

## Acceptance Criteria

- [ ] The \`ProjectMembership\` add view renders without errors.
- [ ] The database schema includes the \`company_id\` column in the \`projects_project\` table.
- [ ] Test coverage is maintained or improved.
- [ ] Documentation is updated if necessary.

## Additional Context

- The issue might be caused by a missing or incomplete migration for the \`projects\` app.
- Ensure that the database schema is consistent with the model definitions.

"

gh issue create --repo $repo --title $title --body $body
```

```fish
gh label create "projects" --description "Issues related to the projects app" --color "#1D76DB"
gh issue edit 74 --add-label "bug,django,database,projects,help wanted"
```
