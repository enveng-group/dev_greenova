# gh issue create template for Greenova Repository

```fish

set repo "https://github.com/enveng-group/dev_greenova"
set title "Bug: Fix Failing Test for Company Deletion by Admin in TestCompanyDeletion"
set body "
## Description

The test \`TestCompanyDeletion::test_company_delete_by_admin\` is failing because the company deletion view redirects instead of allowing access to the delete page for a non-owner admin. The test expects a status code of 200 but receives a 302 redirect.

## Current Behavior

- The test fails with the following error:
  \`\`\`
  assert 302 == 200
  +  where 302 = <HttpResponseRedirect status_code=302, \"text/html; charset=utf-8\", url=\"/company/1/\">.status_code
  \`\`\`

- This indicates that the non-owner admin is being redirected instead of being allowed to access the delete page.

## Expected Behavior

- Non-owner admins should be able to access the company delete page without being redirected.

## Steps to Reproduce

1. Run the following pytest command:
   \`\`\`bash
   pytest -p vscode_pytest -xvs --cov=greenova --cov-report=term-missing --no-cov-on-fail --reuse-db --rootdir=/workspaces/greenova /workspaces/greenova/greenova/company/test_company.py::TestCompanyDeletion::test_company_delete_by_admin[company_admin]
   \`\`\`
2. Observe the test failure.

## Technical Context

- **Django Version**: 4.1.13
- **Python Version**: 3.9.21
- **Affected Module/App**: \`company\`
- **Test File**: \`greenova/company/test_company.py\`

## Proposed Implementation

- Verify the permissions logic in the \`delete\` view of the \`company\` app to ensure non-owner admins are allowed to access the delete page.
- Update the view to handle permissions correctly for non-owner admins.
- Update the test if necessary to align with the expected behavior.

## Acceptance Criteria

- [ ] The test \`TestCompanyDeletion::test_company_delete_by_admin\` passes successfully.
- [ ] Non-owner admins can access the company delete page without being redirected.
- [ ] Test coverage is maintained or improved.

## Additional Context

- The issue might be related to incorrect permissions or redirection logic in the \`delete\` view.
- Ensure that the permissions align with the project's requirements for admin roles.

## Labels

bug, testing, company, django, permissions, help wanted, good first issue
"

gh issue create --repo $repo --title $title --body $body
```
