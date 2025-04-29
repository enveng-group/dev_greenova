# Greenova Project Plan - User Feedback Implementation

This plan organizes user feedback from `notes.txt` into actionable GitHub
issues, grouped by milestones. Each issue includes suggested labels and project
fields for tracking in GitHub Project ID 8.

Prompt: please generate the github issue by updating github-issue-tempalte.md so i can copy and paste in fish terminal and use gh-cli

---

## Milestone 1: Core Bug Fixes & UI Cleanup (High Priority) [Effort: 13] (Release: v0.0.6)

**Description:** This milestone focuses on resolving critical bugs affecting core functionality like obligation editing, navigation, and filtering, along with initial UI cleanup based on immediate user feedback. The goal is to stabilize the application's essential features.
**Due Date:** June 10, 2025

### Issue 1.1: Fix Obligation Edit Functionality

- **Title:** `bug: Obligation update view fails with AttributeError`
- **Description:** The obligation update view
  (`/obligations/update/<obligation_id>/`) throws an
  `AttributeError: 'Obligation' object has no attribute 'responsibilities'`
  when accessed via GET request. This prevents users from editing existing
  obligations.
- **Details:**

  ```
  Traceback (most recent call last):
    File "/home/ubuntu/greenova-0.0.5/.venv/lib/python3.9/site-packages/django/core/handlers/exception.py", line 56, in inner
      response = get_response(request)
    # ... (traceback continues) ...
    File "/home/ubuntu/greenova-0.0.5/greenova/obligations/forms.py", line 403, in __init__
      self.fields['responsibilities'].initial = instance.responsibilities.all()

  Exception Type: AttributeError at /obligations/update/PCEMP-51/
  Exception Value: 'Obligation' object has no attribute 'responsibilities'
  ```

- **Affected Module/App:** `obligations`
- **Affected Files (Estimate):**
  - `/workspaces/greenova/greenova/obligations/views.py`
  - `/workspaces/greenova/greenova/obligations/forms.py`
  - `/workspaces/greenova/greenova/obligations/models.py`
  - `/workspaces/greenova/greenova/obligations/templates/obligations/obligation_form.html`
    (or similar update template)
- **Labels:** `bug`, `django`, `obligations`, `forms`, `priority-critical`
- **Project Fields:**
  - Status: `Sort`
  - Priority: `P1`
  - Size: `M`
  - Effort: `3`

### Issue 1.2: Fix Breadcrumbs Navigation

- **Title:** `bug: Breadcrumbs navigation is not functional`
- **Description:** The breadcrumbs navigation component is not working as
  expected, potentially leading users incorrectly or not updating based on the
  current view.
- **Affected Module/App:** `theme`, `core` (likely base templates)
- **Affected Files (Estimate):**
  - `/workspaces/greenova/greenova/theme/templates/theme/base.html` (or other
    base templates)
  - `/workspaces/greenova/greenova/theme/templatetags/` (if custom tags are
    used)
  - `/workspaces/greenova/greenova/core/views.py` (if context processors
    involved)
  - `/workspaces/greenova/greenova/theme/static/css/`
- **Labels:** `bug`, `ui`, `theme`, `navigation`, `priority-high`
- **Project Fields:**
  - Status: `Sort`
  - Priority: `P1`
  - Size: `S`
  - Effort: `2`

### Issue 1.3: Fix Obligation Overview Filter Logic

- **Title:**
  `bug: Obligation overview filters (search, status, phase, sort) are broken`
- **Description:** The filtering and sorting mechanisms on the obligation
  overview page are not functioning correctly. This includes search, status
  filtering, phase filtering, and sorting.
- **Affected Module/App:** `obligations`
- **Affected Files (Estimate):**
  - `/workspaces/greenova/greenova/obligations/views.py` (Overview view)
  - `/workspaces/greenova/greenova/obligations/templates/obligations/obligation_list.html`
    (or overview template)
  - `/workspaces/greenova/greenova/obligations/forms.py` (if filters use forms)
  - `/workspaces/greenova/greenova/theme/static/js/` (if JS/HTMX involved in
    filtering)
- **Labels:** `bug`, `django`, `ui`, `obligations`, `filters`, `priority-high`
- **Project Fields:**
  - Status: `Sort`
  - Priority: `P1`
  - Size: `M`
  - Effort: `3`

### Issue 1.4: Fix Procedure Charts Horizontal Scroll

- **Title:**
  `bug: Horizontal scroll bar for procedure charts behaves incorrectly`
- **Description:** The horizontal scroll bar for procedure charts is not
  working correctly. Clicking the left scroll button performs the same action
  as the right scroll button. Note: This might be superseded by the gallery
  view implementation (See Issue 2.3). Investigate if fix is needed or if
  gallery view replaces this.
- **Affected Module/App:** `procedures`, `theme` (potentially JS/CSS)
- **Affected Files (Estimate):**
  - `/workspaces/greenova/greenova/procedures/templates/procedures/` (chart
    template)
  - `/workspaces/greenova/greenova/theme/static/js/` (charting library or
    custom scroll JS)
  - `/workspaces/greenova/greenova/theme/static/css/` (styling for chart
    container/scroll)
- **Labels:** `bug`, `ui`, `charts`, `procedures`, `javascript`, `css`,
  `priority-medium`
- **Project Fields:**
  - Status: `Sort`
  - Priority: `P2`
  - Size: `S`
  - Effort: `2`

### Issue 1.5: Address General UI/CSS Tag Issues

- **Title:** `task: Investigate and fix general UI and CSS tag issues`
- **Description:** User feedback mentioned "ui and css tags issues in new
  milestone too". This requires investigation to identify the specific problems
  and address them. Could involve inconsistent styling, incorrect HTML tag
  usage, or CSS conflicts.
- **Affected Module/App:** Potentially multiple, `theme` likely involved.
- **Affected Files (Estimate):**
  - `/workspaces/greenova/greenova/theme/static/css/`
  - Various templates across apps
    (`/workspaces/greenova/greenova/*/templates/`)
  - `/workspaces/greenova/greenova/theme/templates/theme/` (base templates,
    partials)
- **Labels:** `task`, `ui`, `css`, `html`, `theme`, `priority-medium`
- **Project Fields:**
  - Status: `Sort`
  - Priority: `P2`
  - Size: `M`
  - Effort: `3`

---

## Milestone 1B: Secondary Bug Fixes (High Priority) [Effort: 4] (Release: v0.0.7)

**Description:** Addresses important but less critical bugs identified in the admin panel and obligation forms after the initial stabilization.
**Due Date:** June 24, 2025

### Issue 1B.1: Fix Responsibilities Display in Admin (#98)
- **Title:** `bug: Responsibilities not displaying in the admin panel`
- **Ref:** #98
- **Labels:** `bug`, `django`, `database`, `priority-high`, `admin`
- **Project Fields:** Priority: `P1`, Size: `S`, Effort: `2`, Status: `Sort`

### Issue 1B.2: Fix Obligation Form Recurring Field Bug (#82)
- **Title:** `bug: Obligation form has mandatory recurring field and inability to set N/A`
- **Ref:** #82
- **Labels:** `bug`, `django`, `ui`, `priority-medium`, `forms`, `obligations`
- **Project Fields:** Priority: `P2`, Size: `S`, Effort: `2`, Status: `Sort`

---

## Milestone 2A: UI/UX Core Improvements & Cleanup (Medium Priority) [Effort: 17] (Release: v0.1.0)

**Description:** This milestone focuses on implementing key UI changes requested in feedback, refining existing views (Procedure, Obligation List/Overview), redesigning navigation, and removing obsolete sections (Responsibility Distribution, old Filter section).
**Due Date:** August 5, 2025

### Issue 2A.1: Redesign Navigation Bar and Header (was 2.1)

- **Title:** `enhancement: Redesign main navigation bar and header`
- **Description:** Consolidate the header elements. Remove the redundant
  'header', leaving only 'banner-header'. Make the 'banner-header' smaller in
  height and stretch to full width. Move breadcrumbs into the 'banner-header',
  possibly using a dropdown menu. Improve overall styling and design of the nav
  bar. Convert the light/dark mode toggle to use icons instead of text/buttons.
- **Sub-tasks:**
  - Remove redundant 'header'.
  - Resize and restyle 'banner-header'.
  - Integrate breadcrumbs into 'banner-header'.
  - Implement light/dark mode icons.
  - General styling improvements.
- **Affected Module/App:** `theme`, `core` (base templates)
- **Affected Files (Estimate):**
  - `/workspaces/greenova/greenova/theme/templates/theme/base.html`
  - `/workspaces/greenova/greenova/theme/templates/theme/partials/header.html`
    (or similar)
  - `/workspaces/greenova/greenova/theme/templates/theme/partials/breadcrumbs.html`
    (or similar)
  - `/workspaces/greenova/greenova/theme/static/css/`
  - `/workspaces/greenova/greenova/theme/static/js/` (for dropdowns, theme
    toggle)
- **Labels:** `enhancement`, `refactoring`, `ui`, `ux`, `theme`, `css`,
  `navigation`, `priority-medium`
- **Project Fields:**
  - Status: `Set In Order`
  - Priority: `P2`
  - Size: `L`
  - Effort: `5`

### Issue 2A.2: Improve Procedure View Layout (was 2.2)

- **Title:**
  `enhancement: Improve layout and functionality of the Procedure view`
- **Description:** Modify the procedure view page: Move the 'procedure by
  status' chart to the top of the page. Add a toggle mechanism (e.g., button or
  accordion) to allow users to expand/shrink the 'filter-header' section.
- **Affected Module/App:** `procedures`
- **Affected Files (Estimate):**
  - `/workspaces/greenova/greenova/procedures/views.py`
  - `/workspaces/greenova/greenova/procedures/templates/procedures/procedure_detail.html`
    (or similar view template)
  - `/workspaces/greenova/greenova/theme/static/css/`
  - `/workspaces/greenova/greenova/theme/static/js/` (for toggle)
- **Labels:** `enhancement`, `ui`, `ux`, `procedures`, `charts`,
  `priority-medium`
- **Project Fields:**
  - Status: `Set In Order`
  - Priority: `P2`
  - Size: `M`
  - Effort: `3`

### Issue 2A.3: Refine Obligation List View (was 2.4)

- **Title:**
  `enhancement: Refine columns and default filter for Obligation list view`
- **Description:** Modify the main obligation list view: Remove the
  'Mechanism', 'Phase', and 'Recurring' columns to allow more space for the
  core 'Obligation' text. Change the default view to only display obligations
  with an "Overdue" status. Provide a clear way for users to reset filters to
  see all obligations.
- **Affected Module/App:** `obligations`
- **Affected Files (Estimate):**
  - `/workspaces/greenova/greenova/obligations/views.py` (List view)
  - `/workspaces/greenova/greenova/obligations/templates/obligations/obligation_list.html`
  - `/workspaces/greenova/greenova/obligations/tables.py` (if using
    django-tables2)
- **Labels:** `enhancement`, `ui`, `ux`, `obligations`, `priority-low`
- **Project Fields:**
  - Status: `Set In Order`
  - Priority: `P3`
  - Size: `S`
  - Effort: `2`

### Issue 2A.4: Improve Obligation Overview UI (was 2.5)

- **Title:** `enhancement: Improve UI for Obligation Overview and Filters`
- **Description:** General UI improvements are needed for the
  'obligation-overview' section and its associated filters based on user
  feedback. This involves reviewing the current layout, styling, and usability
  of this section and implementing necessary changes.
- **Affected Module/App:** `obligations`
- **Affected Files (Estimate):**
  - `/workspaces/greenova/greenova/obligations/templates/obligations/obligation_list.html`
    (or overview template)
  - `/workspaces/greenova/greenova/theme/static/css/`
- **Labels:** `enhancement`, `ui`, `ux`, `obligations`, `filters`,
  `priority-low`
- **Project Fields:**
  - Status: `Set In Order`
  - Priority: `P3`
  - Size: `M`
  - Effort: `3`

### Issue 2A.5: Remove Responsibility Distribution Section (was 2.6)

- **Title:** `enhancement: Remove Responsibility Distribution section`
- **Description:** Remove the "Responsibility Distribution" section from the UI
  as requested by user feedback. Ensure related views, templates, and
  potentially data queries are updated accordingly.
- **Affected Module/App:** `responsibility`, potentially `dashboard` or other
  views displaying this.
- **Affected Files (Estimate):**
  - Templates displaying the section (e.g.,
    `/workspaces/greenova/greenova/dashboard/templates/dashboard/dashboard.html`)
  - `/workspaces/greenova/greenova/responsibility/views.py` (if specific view
    exists)
  - `/workspaces/greenova/greenova/responsibility/templates/responsibility/`
- **Labels:** `enhancement`, `ui`, `responsibility`, `priority-low`
- **Project Fields:**
  - Status: `Set In Order`
  - Priority: `P3`
  - Size: `S`
  - Effort: `2`

### Issue 2A.6: Remove Main Filter Section (Confirmation Needed) (was 2.7)

- **Title:** `enhancement: Remove main filter section (Confirmation Needed)`
- **Description:** User feedback requested removing the "filter section
  altogether". This conflicts slightly with Issue 2.2 (adding a toggle to the
  _procedure_ filter header). Confirm which filter section is intended for
  removal (likely a main/global one associated with the old header structure)
  and remove it.
- **Affected Module/App:** `theme`, `core` (base templates), potentially
  specific apps.
- **Affected Files (Estimate):**
  - `/workspaces/greenova/greenova/theme/templates/theme/base.html` (or where
    the global filter resides)
  - `/workspaces/greenova/greenova/theme/static/css/`
- **Labels:** `enhancement`, `refactoring`, `ui`, `filters`, `priority-low`,
  `question`
- **Project Fields:**
  - Status: `Set In Order`
  - Priority: `P3`
  - Size: `S`
  - Effort: `2`

---

## Milestone 2B: Major Refactoring & Technical Improvements (Medium Priority) [Effort: 24] (Release: v0.2.0)

**Description:** This milestone concentrates on foundational technical improvements. It includes integrating Sass, migrating templates to Jinja2, enhancing the PostCSS build process, reviewing responsive design, and evaluating alternative UI/CSS approaches.
**Due Date:** October 7, 2025

### Issue 2B.1: Review and Optimize Responsive Design (Mobile-First) (was 2.9)

- **Title:**
  `enhancement: Review and optimize responsive design (Mobile-First)`
- **Description:** Conduct a thorough review of the application's
  responsiveness across various screen sizes, focusing on a mobile-first
  approach. Identify and fix layout issues, usability problems, and styling
  inconsistencies on smaller devices.
- **Affected Module/App:** `theme`, `css`, potentially all templates.
- **Affected Files (Estimate):**
  - `/workspaces/greenova/greenova/theme/static/css/` (main CSS, Tailwind
    config related files)
  - All templates (`/workspaces/greenova/greenova/*/templates/`)
- **Labels:** `enhancement`, `ui`, `ux`, `css`, `accessibility`, `mobile`,
  `priority-medium`
- **Project Fields:**
  - Status: `Shine`
  - Priority: `P2`
  - Size: `L`
  - Effort: `5`

### Issue 2B.2: Integrate Sass and Enhance PostCSS Setup (was 2.10)

- **Title:** `enhancement: Integrate Sass and enhance PostCSS build process`
- **Description:** Implement Sass (`.scss`) for structuring custom CSS,
  potentially overriding or complementing PicoCSS styles. Enhance the existing
  `django-tailwind` PostCSS process by adding plugins like `autoprefixer` and
  `postcss-nesting` to improve browser compatibility and enable modern CSS
  features, focusing on a mobile-first responsive design approach.
- **Sub-tasks:**
  - Install `sass`, `autoprefixer`, `postcss-nesting`.
  - Configure `django-tailwind` or the build process to compile Sass files
    (`theme/static/scss/`) into the main CSS output
    (`theme/static/css/dist/styles.css`).
  - Configure `tailwind.config.js` and `postcss.config.js` (if needed,
    `django-tailwind` might manage this) to include the new plugins.
  - Create initial Sass structure (e.g., `_variables.scss`, `_base.scss`,
    `_components.scss`) within `theme/static/scss/`.
  - Ensure the build process correctly integrates Sass output with TailwindCSS
    and applies PostCSS plugins.
  - Update documentation regarding the new styling workflow.
- **Affected Module/App:** `theme`, Build process configuration
- **Affected Files (Estimate):**
  - `/workspaces/greenova/package.json` (for npm dependencies)
  - `/workspaces/greenova/tailwind.config.js`
  - `/workspaces/greenova/postcss.config.js` (potentially, or handled by
    django-tailwind settings)
  - `/workspaces/greenova/greenova/theme/apps.py` (or wherever django-tailwind
    is configured)
  - `/workspaces/greenova/greenova/settings/base.py` (if django-tailwind
    settings need adjustment)
  - New files: `/workspaces/greenova/greenova/theme/static/scss/` (e.g.,
    `main.scss`, `_variables.scss`)
  - `/workspaces/greenova/greenova/theme/templates/theme/base.html` (to link
    the final CSS)
  - `/workspaces/greenova/Makefile` or other build scripts if customization
    beyond django-tailwind is needed.
- **Labels:** `enhancement`, `refactoring`, `css`, `sass`, `postcss`,
  `tailwind`, `build`, `ui`, `ux`, `priority-medium`
- **Project Fields:**
  - Status: `Set In Order`
  - Priority: `P2`
  - Size: `L`
  - Effort: `5`

### Issue 2B.3: Migrate Templates from DTL to Jinja2 (was 2.11)

- **Title:**
  `refactor: Migrate templates from Django Template Language (DTL) to Jinja2`
- **Description:** Refactor all existing HTML templates across the project to
  use the Jinja2 templating engine instead of the default Django Template
  Language. This involves updating syntax for variables, tags, filters, and
  template inheritance. Ensure Django is configured correctly to use Jinja2 as
  the primary template backend.
- **Affected Module/App:** `theme`, all apps using templates (`landing`,
  `obligations`, `procedures`, `dashboard`, `profiles`, etc.)
- **Affected Files (Estimate):**
  - All `.html` files under `/workspaces/greenova/greenova/*/templates/`
  - `/workspaces/greenova/greenova/settings/base.py` (for Jinja2 configuration)
- **Labels:** `refactoring`, `templates`, `jinja2`, `django`, `priority-medium`
- **Project Fields:**
  - Status: `Set In Order`
  - Priority: `P2`
  - Size: `XL`
  - Effort: `8`

### Issue 2B.4: Evaluate django-cotton (#40) (was 6.7)

- **Title:** `research: Evaluate django-cotton for component-based UI design`
- **Ref:** #40
- **Labels:** `enhancement`, `django`, `ui`, `research`
- **Project Fields:** Priority: `P3`, Size: `M`, Effort: `3`, Status: `Sort`

### Issue 2B.5: Leverage CSS Frameworks More Effectively (#38) (was 6.8)

- **Title:** `enhancement: Leverage CSS Frameworks and Libraries More Effectively`
- **Ref:** #38
- **Labels:** `enhancement`, `django`, `CSS`, `ui`, `theme`
- **Project Fields:** Priority: `P3`, Size: `M`, Effort: `3`, Status: `Sort`

---

## Milestone 2C: Feature Implementation & UI Enhancements (Medium Priority) [Effort: 11] (Release: v0.3.0)

**Description:** This milestone focuses on building the new gallery view for procedures, enhancing chart interactivity, adding interactive links, and cleaning up the dashboard project selection.
**Due Date:** October 28, 2025

### Issue 2C.1: Implement Gallery View for Procedures (was 2.3)

- **Title:** `enhancement: Display procedures in a gallery view`
- **Description:** Replace the current procedure chart display (potentially
  with the problematic scroll bar - see Issue 1.4) with a gallery view. Display
  procedures in rows (e.g., three per row) on a single page, allowing users to
  see multiple procedures at once without horizontal scrolling.
- **Affected Module/App:** `procedures`
- **Affected Files (Estimate):**
  - `/workspaces/greenova/greenova/procedures/views.py`
  - `/workspaces/greenova/greenova/procedures/templates/procedures/procedure_gallery.html`
    (new or modified template)
  - `/workspaces/greenova/greenova/procedures/urls.py`
  - `/workspaces/greenova/greenova/theme/static/css/`
- **Labels:** `enhancement`, `ui`, `ux`, `procedures`, `priority-medium`
- **Project Fields:**
  - Status: `Set In Order`
  - Priority: `P2`
  - Size: `M`
  - Effort: `3`

### Issue 2C.2: Enhance Chart Interactivity (was 2.8)

- **Title:** `enhancement: Add more interactivity to charts`
- **Description:** Improve user interaction with charts throughout the
  application. This could include tooltips on hover, clickable elements linking
  to details, zoom/pan functionality, or dynamic updates based on user input.
  Specific charts to target need identification.
- **Affected Module/App:** Multiple apps using charts (`dashboard`,
  `procedures`, `obligations`, etc.)
- **Affected Files (Estimate):**
  - `/workspaces/greenova/greenova/theme/static/js/` (charting library
    integration, custom JS)
  - Templates where charts are rendered (e.g., `dashboard`, `procedures`,
    `obligations`)
  - Views providing chart data (`/workspaces/greenova/greenova/*/views.py`)
- **Labels:** `enhancement`, `ui`, `ux`, `charts`, `javascript`, `priority-low`
- **Project Fields:**
  - Status: `Shine`
  - Priority: `P3`
  - Size: `L`
  - Effort: `5`

### Issue 2C.3: Add Interactive Status Links in Procedure View (#37) (was 6.9)

- **Title:** `enhancement: Add Interactive Hyperlinks for Status Counts in Procedure View`
- **Ref:** #37
- **Labels:** `enhancement`, `django`, `ux`, `ui`, `procedures`
- **Project Fields:** Priority: `P3`, Size: `S`, Effort: `2`, Status: `Sort`

### Issue 2C.4: Clean up Project Selection View (#31) (was 6.10)

- **Title:** `enhancement: Clean up Project Selection View on Dashboard`
- **Ref:** #31
- **Labels:** `enhancement`, `django`, `CSS`, `ui`, `dashboard`
- **Project Fields:** Priority: `P3`, Size: `S`, Effort: `1`, Status: `Sort`

---

## Milestone 3: Planning & Documentation (Low Priority) [Effort: 9] (Release: v0.3.1)

**Description:** This milestone focuses on foundational planning and documentation tasks essential for long-term project health and understanding. Activities include defining user personas, visualizing user journeys, refining process templates (like bug reports), and coordinating design elements such as the project logo.
**Due Date:** November 18, 2025

### Issue 3.1: Define User Personas

- **Title:** `docs: Define user personas for Greenova`
- **Description:** Document the different user personas for the Greenova
  application based on user roles and needs (e.g., CX Level, Manager, Worker).
  Detail their goals, typical tasks, and how they interact with the application
  (macro charts vs. micro views vs. data entry).
- **Affected Module/App:** `docs`
- **Labels:** `documentation`, `planning`, `ux`, `priority-low`
- **Project Fields:**
  - Status: `Standardize`
  - Priority: `P3`
  - Size: `M`
  - Effort: `3`

### Issue 3.2: Visualize User Journey

- **Title:** `docs: Visualize user journey using Mermaid diagrams`
- **Description:** Create Mermaid diagrams to visualize key user journeys
  within the Greenova application, based on the defined personas (Issue 3.1).
  This will help understand user flow and identify potential friction points.
- **Affected Module/App:** `docs`
- **Labels:** `documentation`, `planning`, `ux`, `mermaid`, `priority-low`
- **Project Fields:**
  - Status: `Standardize`
  - Priority: `P3`
  - Size: `M`
  - Effort: `3`

### Issue 3.3: Review Bug Report Template

- **Title:**
  `docs: Review and update bug report template regarding 'Evidence' field`
- **Description:** Review the standard bug report template provided in
  `notes.txt`. User feedback mentioned "No Specific Field for 'Evidence'".
  Assess if an 'Evidence' field (for screenshots, logs, etc.) should be
  explicitly added or if existing sections cover this adequately. Update the
  template if necessary.
- **Affected Module/App:** `docs` (template files)
- **Labels:** `documentation`, `planning`, `priority-low`
- **Project Fields:**
  - Status: `Standardize`
  - Priority: `P4`
  - Size: `XS`
  - Effort: `1`

### Issue 3.4: Coordinate Project Logo Design

- **Title:** `task: Coordinate project logo design process`
- **Description:** Manage the process for designing a project logo based on
  user interest. Collect submissions and facilitate voting/selection as per the
  note in `notes.txt`.
- **Affected Module/App:** Project Management / Design
- **Labels:** `task`, `design`, `planning`, `priority-low`
- **Project Fields:**
  - Status: `Standardize`
  - Priority: `P4`
  - Size: `S`
  - Effort: `2`

---

## Milestone 4: Testing & Stability (High Priority) [Effort: 26] (Release: v0.3.2)

**Description:** This milestone is dedicated to fixing the backlog of failing automated tests across various modules (Authentication, Chatbot, Company, UI/Selenium) to ensure application stability and reliability.
**Due Date:** January 13, 2026

### Issue 4.1: Fix Failing Test - Company Creation Requires Login (#72)
- **Title:** `bug: Fix Failing Test for Company Creation Requires Login in TestCompanyViews`
- **Ref:** #72
- **Labels:** `bug`, `django`, `pytest`, `testing`, `company`
- **Project Fields:** Priority: `P1`, Size: `S`, Effort: `2`, Status: `Sort`

### Issue 4.2: Fix Failing Test - Create Conversation View (#71)
- **Title:** `bug: Fix Failing Test for Create Conversation View in TestChatbotViews`
- **Ref:** #71
- **Labels:** `bug`, `django`, `pytest`, `testing`, `chatbot`
- **Project Fields:** Priority: `P1`, Size: `S`, Effort: `2`, Status: `Sort`

### Issue 4.3: Fix Failing Test - Chatbot Home View (#70)
- **Title:** `bug: Fix Failing Test for Chatbot Home View in TestChatbotViews`
- **Ref:** #70
- **Labels:** `bug`, `django`, `pytest`, `testing`, `chatbot`
- **Project Fields:** Priority: `P1`, Size: `S`, Effort: `2`, Status: `Sort`

### Issue 4.4: Fix Failing UI Tests - Chatbot (#69)
- **Title:** `bug: Fix Failing UI Tests for Chatbot in TestChatbotUI`
- **Ref:** #69
- **Labels:** `bug`, `django`, `pytest`, `selenium`, `testing`, `chatbot`, `ui`
- **Project Fields:** Priority: `P1`, Size: `M`, Effort: `3`, Status: `Sort`

### Issue 4.5: Fix Failing Test - TrainingData Model (#68)
- **Title:** `bug: Fix Failing Test for TrainingData Model in TestChatbotModels`
- **Ref:** #68
- **Labels:** `bug`, `django`, `pytest`, `testing`, `chatbot`, `models`
- **Project Fields:** Priority: `P1`, Size: `S`, Effort: `2`, Status: `Sort`

### Issue 4.6: Fix Failing Test - Conversation Flow (#67)
- **Title:** `bug: Fix Failing Test for Conversation Flow in TestChatbotIntegration`
- **Ref:** #67
- **Labels:** `bug`, `django`, `pytest`, `testing`, `chatbot`
- **Project Fields:** Priority: `P1`, Size: `S`, Effort: `2`, Status: `Sort`

### Issue 4.7: Fix Selenium WebDriver Failure in Devcontainer (#62)
- **Title:** `bug: Selenium WebDriver Fails in Devcontainer`
- **Ref:** #62
- **Labels:** `bug`, `Docker`, `selenium`, `testing`
- **Project Fields:** Priority: `P1`, Size: `M`, Effort: `3`, Status: `Sort`

### Issue 4.8: Fix Failing Test - Password Change Requires Login (#61)
- **Title:** `bug: Fix Failing Test for Password Change Requires Login in TestAuthenticationViews`
- **Ref:** #61
- **Labels:** `bug`, `django`, `pytest`, `testing`, `authentication`
- **Project Fields:** Priority: `P1`, Size: `S`, Effort: `2`, Status: `Sort`

### Issue 4.9: Fix Failing Test - Logout Requires Login (#60)
- **Title:** `bug: Fix Failing Test for Logout Requires Login in TestAuthenticationViews`
- **Ref:** #60
- **Labels:** `bug`, `django`, `pytest`, `testing`, `authentication`
- **Project Fields:** Priority: `P1`, Size: `S`, Effort: `2`, Status: `Sort`

### Issue 4.10: Fix Failing Test - Password Reset Request (#59)
- **Title:** `bug: Fix Failing Test for Password Reset Request in TestAccountManagement`
- **Ref:** #59
- **Labels:** `bug`, `django`, `pytest`, `testing`, `authentication`
- **Project Fields:** Priority: `P1`, Size: `S`, Effort: `2`, Status: `Sort`

### Issue 4.11: Fix Failing Test - Login with Email (#57)
- **Title:** `bug: Fix Failing Test for Login with Email in TestAccountManagement`
- **Ref:** #57
- **Labels:** `bug`, `django`, `pytest`, `testing`, `authentication`
- **Project Fields:** Priority: `P1`, Size: `S`, Effort: `2`, Status: `Sort`

### Issue 4.12: Fix Failing Test - User Signup (#56)
- **Title:** `bug: Fix Failing Test for User Signup in TestAccountManagement`
- **Ref:** #56
- **Labels:** `bug`, `django`, `pytest`, `testing`, `authentication`
- **Project Fields:** Priority: `P1`, Size: `S`, Effort: `2`, Status: `Sort`

### Issue 4.13: Fix Failing Test - Password Reset Confirmation (#47)
- **Title:** `bug: Password Reset Confirmation Test Failing with Incorrect URL`
- **Ref:** #47
- **Labels:** `bug`, `pytest`, `testing`, `authentication`
- **Project Fields:** Priority: `P1`, Size: `S`, Effort: `2`, Status: `Sort`

---

## Milestone 5: New Feature Implementation (Medium Priority) [Effort: 21] (Release: TBD)

**Description:** This milestone focuses on developing significant new application modules: Company Management, Inspections, and Auditing.
**Due Date:** March 17, 2026

### Issue 5.1: Implement Company Management Feature (#87)
- **Title:** `feature: Implement company management feature with user roles`
- **Ref:** #87
- **Labels:** `enhancement`, `django`, `ui`, `testing`, `database`, `company`, `priority-high`
- **Project Fields:** Priority: `P1`, Size: `XL`, Effort: `8`, Status: `Sort`

### Issue 5.2: Create Inspection Application (#54)
- **Title:** `feature: Create Inspection Application with Recurring Frequency`
- **Ref:** #54
- **Labels:** `feature`, `django`, `database`, `models`, `priority-medium`
- **Project Fields:** Priority: `P2`, Size: `L`, Effort: `5`, Status: `Sort`

### Issue 5.3: Create Auditing Application (#53)
- **Title:** `feature: Create Auditing Application for Compliance and Non-Conformance`
- **Ref:** #53
- **Labels:** `enhancement`, `feature`, `django`, `database`, `models`, `priority-medium`
- **Project Fields:** Priority: `P2`, Size: `XL`, Effort: `8`, Status: `Sort`

---

## Milestone 6: Core Data Model & Feature Enhancements (Medium Priority) [Effort: 13] (Release: TBD)

**Description:** This milestone includes enhancements to core data models (Obligations, Responsibility, Users) and related features based on existing GitHub issues.
**Due Date:** April 14, 2026

### Issue 6.1: Add Obligation Type Domain (#96) (was 6.2)

- **Title:** `enhancement: Add New Domain "Obligation Type" to Obs Register`
- **Ref:** #96
- **Labels:** `enhancement`, `django`, `priority-medium`, `obligations`, `models`
- **Project Fields:** Priority: `P2`, Size: `M`, Effort: `3`, Status: `Sort`

### Issue 6.2: Modify Responsibility Table Input (#89) (was 6.3)

- **Title:** `enhancement: Modify responsibility table to use text input instead of dropdown`
- **Ref:** #89
- **Labels:** `enhancement`, `refactoring`, `database`, `priority-high`, `responsibility`, `ui`
- **Project Fields:** Priority: `P1`, Size: `M`, Effort: `3`, Status: `Sort`

### Issue 6.3: Add User Profile Role Relationship & Alerts (#88) (was 6.4)

- **Title:** `enhancement: Add user profile role relationship and overdue alerts`
- **Ref:** #88
- **Labels:** `enhancement`, `django`, `ui`, `database`, `priority-high`, `users`, `profiles`
- **Project Fields:** Priority: `P1`, Size: `L`, Effort: `5`, Status: `Sort`

### Issue 6.4: Remove Compliance/Non-Conformance Comments (#51) (was 6.6)

- **Title:** `enhancement: Remove Compliance and Non-Conformance Comments from Obligation Model`
- **Ref:** #51
- **Labels:** `enhancement`, `django`, `models`, `obligations`
- **Project Fields:** Priority: `P3`, Size: `S`, Effort: `2`, Status: `Sort`
