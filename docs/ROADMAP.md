<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Greenova Roadmap](#greenova-roadmap)
  - [Phase 1: Core User and Project Management](#phase-1-core-user-and-project-management)
  - [Phase 2: Advanced Features and Reporting](#phase-2-advanced-features-and-reporting)
  - [Phase 3: Modularization, UI/UX, and Auditing](#phase-3-modularization-uiux-and-auditing)
  - [References](#references)
    - [✅ Phase 1: Setup & Auth](#-phase-1-setup--auth)
    - [🛠️ Phase 2: Core Features](#-phase-2-core-features)
    - [📊 Phase 3: Dashboards & Navigation](#-phase-3-dashboards--navigation)
    - [📈 Phase 4: Visuals & Final Polish](#-phase-4-visuals--final-polish)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Greenova Roadmap

## Phase 1: Core User and Project Management

1. Log in using the credentials created during setup
2. Create projects and define environmental mechanisms
3. Add obligations related to your projects
4. Assign responsibilities to users
5. Monitor compliance status
6. CRUD user profiles and company information
7. Drill down into mechanisms, then into procedures, then into obligations for
   detailed information
   - Perform CRUD operations on obligations
8. When hovering over the overdue obligations card, a tooltip will display a
   list of overdue obligations
   - Each overdue obligation will be listed and clickable, linking to its
     detail page
   - You can edit individual obligation records from their detail pages
   - Full CRUD operations are supported for overdue obligations

## Phase 2: Advanced Features and Reporting

- Generate charts and data visualizations using matplotlib (static) and Plotly
  (interactive)
- Integrate static and interactive charts into dashboard and reporting views
- Use protobuf3 for data serialization between backend and frontend, especially
  for chart data
- Implement compliance summaries, trend analysis, and printable reports
- Add notifications (email and SMS alerts)
- Support multi-tenancy (multiple organizations)
- Performance optimization (database indexing, query optimization)

## Phase 3: Modularization, UI/UX, and Auditing

- Modularize auditing and comment tracking (see PR #145)
- Refactor header bar and UI components for accessibility and responsiveness
  (see PR #149)
- Enhance filtering, sorting, and HTMX/JS logic for obligations and procedures
  (see PR #150)
- Add mechanism and procedure charts (see PR #154)
- Improve scrollable chart areas and UI consistency (see PR #148)
- Integrate authentication improvements and allauth (see PR #131)
- Enhance import/export and data validation (see PR #128)
- Add developer tooling, syntax checking, and bash aliases (see PR #103)

---

## References

- [Django Documentation](https://docs.djangoproject.com/)
- [HTMX Documentation](https://htmx.org/)
- [Greenova GitHub Pull Requests](https://github.com/enveng-group/dev_greenova/pulls)
- [Greenova GitHub Issues](https://github.com/enveng-group/dev_greenova/issues)
- [Greenova Project Board](https://github.com/users/enveng-group/projects/8) Hi
  Raheel,

Thanks again—great to have you on board!

To get started, please **fork** the Greenova repo to your GitHub account and
**clone your forked version** locally: 🔗
<https://github.com/enveng-group/dev_greenova>

---

🔧 **Next Steps**

After setting up your environment (see `README`), you can begin working through
the following tasks. Please submit a **pull request** after each task and
assign **@enveng-group** as the reviewer.

---

### ✅ Phase 1: Setup & Auth

1. **Fork, Clone & Setup**

   - Set up local dev environment and confirm tests/pre-commit hooks run.

2. **Integrate `django-allauth` with MFA**
   - Add MFA, refactor templates with PicoCSS + semantic HTML, ensure WCAG 2.1
     AA compliance, and add runtime type checks/tests.

---

### 🛠️ Phase 2: Core Features

1. **Projects & Mechanisms CRUD**

   - Build user-facing CRUD with permissions, type annotations, and accessible
     forms.

2. **Obligations CRUD**

   - Add validation, accessibility, and tests.

3. **Responsibility Assignment**
   - UI for assigning obligations to users/groups with permission logic.

---

### 📊 Phase 3: Dashboards & Navigation

1. **Compliance Dashboard**

   - Refactor layout, add filtering, drill-down, and accessibility.

1. **Drill-down Navigation**

   - Mechanism → Procedure → Obligation with filtering/sorting.

1. **Overdue Tooltip**

   - Add interactive, accessible tooltip for overdue items.

1. **Procedure Charts → Grid View**

   - Refactor procedure charts into a responsive grid layout.

### 📈 Phase 4: Visuals & Final Polish

1. **Charts & Visualizations**

   - Integrate matplotlib + Plotly, serialize via protobuf3.

1. **Protobuf3 Schemas**

   - Implement and maintain backend/external schemas.

1. **Code Review & Docs**

   - Refactor for maintainability, ensure 80%+ test coverage, validate type

     stubs, and update docs.

---

Let me know if you have any questions or want to sync before the kick-off on
**Monday, 26 May**.

Best, Adrian Gallo Greenova Maintainer
