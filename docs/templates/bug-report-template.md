# Greenova Bug Report Template

## Instructions

This template will help you provide all the information needed to quickly
address your issue. Please fill out as many sections as possible with detailed
information.

## Bug Report Details

### 1. Summary

- **Title:** Obligation form issues: mandatory recurring field and inability to
  customize obligation numbers

  - _Example: "Dashboard fails to load environmental metrics when filtering by
    project"_
  - _Tip: Include the specific feature and the problem in your title_

- **Description:** Users are experiencing two issues with the Obligation
  registration form: (1) the "recurring obligation" checkbox is required even
  for non-recurring obligations, and (2) users cannot customize obligation
  numbers to use specific formats like "W6875 Condition 1.6a" instead of the
  auto-generated "PCEMP-237" format.
  - _Example: "When applying the project filter on the dashboard, environmental
    metrics don't update and the page shows a loading spinner indefinitely."_
  - _Tip: Focus on what happened, when it happened, and the context_

### 2. Environment

- **Application Version:** Latest production deployment of Greenova
  environmental management system

  - _How to find it: Check the footer of any Greenova page or look at the
    "About" section in settings_

- **Operating System:** Various (issue is application-specific, not
  OS-dependent)

  - _Windows: Click Start > Settings > System > About_
  - _Linux: Open Terminal and type `lsb_release -a` or `cat /etc/os-release`_

- **Browser:** Various (issue is server-side, not browser-specific)

- **Device:** Desktop/Laptop

### 3. Steps to Reproduce

1. Log into the Greenova application
2. Navigate to the Obligation registration form
3. Attempt to create a new obligation
4. Try to leave the "recurring obligation" checkbox unchecked
5. Notice that the form cannot be submitted without checking this box
6. Also observe that the obligation number field cannot be edited to use custom
   formats like "W6875 Condition 1.6a"

### 4. Expected vs Actual Behavior

- **Expected:**

  1. The "recurring obligation" checkbox should be optional, allowing users to
     submit the form without checking it
  2. Users should be able to customize obligation numbers to match specific
     formats like "W6875 Condition 1.6a"

- **Actual:**
  1. The "recurring obligation" checkbox is mandatory, forcing users to
     incorrectly mark non-recurring obligations as recurring
  2. Obligation numbers are auto-generated in the "PCEMP-XXX" format and cannot
     be customized

### 5. Impact

- **Severity:** Medium
- **Scope:** All users creating or editing obligations
- **Business Impact:**
  - Data integrity issues as non-recurring obligations are incorrectly marked
    as recurring
  - Difficulty in navigating and identifying specific obligations due to
    inability to use custom obligation numbers
  - Reduced usability of the environmental obligations register for projects
    where specific numbering formats are required by regulatory documents

### 6. Relevant Information

- **Error Messages:** None (form validation prevents submission)
- **Screenshots/Videos:** [Not provided]
- **Code References:**
  - Issue likely exists in the `ObligationForm` class in
    `/workspaces/greenova/greenova/obligations/forms.py`
  - The recurring_obligation field is set as `required=True`
  - Obligation numbers are validated and auto-generated in the `Obligation`
    model in `/workspaces/greenova/greenova/obligations/models.py`

### 7. Possible Solutions

1. Modify the `ObligationForm` to set `recurring_obligation` field's `required`
   attribute to `False`
2. Update the `Obligation` model and form to allow custom obligation numbers
   that don't follow the PCEMP-XXX pattern
3. Add a configuration option to toggle between auto-generated and custom
   obligation numbering

### 8. Additional Context

- This issue affects users working with the primary environmental mechanism
  'W6875/2023/1' who need to reference specific conditions like "Condition
  1.2", "Condition 1.2a", etc.
- User is currently adding obligations under this mechanism with incorrect
  numbering (PCEMP-237 instead of the desired W6875 Condition 1.6a)

### 9. Reporter Information

- **Name:** [User reporting via conversation]
- **Role:** Environmental compliance user
- **Date Reported:** [Current date]
