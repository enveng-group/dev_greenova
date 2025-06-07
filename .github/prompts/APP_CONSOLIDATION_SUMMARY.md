<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Greenova App Consolidation Summary](#greenova-app-consolidation-summary)
  - [Deprecated Apps and Prompts](#deprecated-apps-and-prompts)
    - [DEPRECATED: `users` app](#deprecated-users-app)
    - [DEPRECATED: `auditing` app](#deprecated-auditing-app)
  - [Active App Ecosystem (Post-Consolidation)](#active-app-ecosystem-post-consolidation)
    - [Foundation Apps](#foundation-apps)
    - [Business Process Apps](#business-process-apps)
    - [Organizational Apps](#organizational-apps)
    - [Support Apps](#support-apps)
  - [Updated Business Process Mapping](#updated-business-process-mapping)
  - [Data Flow (Updated)](#data-flow-updated)
  - [Dependencies Update](#dependencies-update)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Greenova App Consolidation Summary

## Deprecated Apps and Prompts

### DEPRECATED: `users` app

- **Status**: Functionality consolidated into `core` app
- **Reason**: User management should be centralized in the core foundation
- **Prompt**: No dedicated prompt was created (never existed)
- **Migration**: All user profile, authentication, and user management features moved to `core`

### DEPRECATED: `auditing` app

- **Status**: Functionality consolidated into `core` app
- **Reason**: Audit trail functionality should be globally available from core services
- **Prompt**: `09_auditing_app_refactor.prompt.md` - DEPRECATED
- **Migration**: All audit models, views, signals, and middleware moved to `core`

## Active App Ecosystem (Post-Consolidation)

### Foundation Apps

1. **core** - Authentication, user management, auditing, base templates, shared utilities
2. **navigation** - Centralized navigation UI components
3. **sidebar** - Centralized sidebar UI components
4. **protobuf** - Protocol Buffer schema management

### Business Process Apps

5. **dashboard** - Main dashboard interface & navigation
6. **obligations** - Comprehensive obligation management
7. **projects** - Project & environmental mechanism management
8. **mechanisms** - Environmental control measures
9. **responsibilities** - User role assignment & responsibility management
10. **audits** - Compliance verification and audit events
11. **procedures** - Standard operating procedures
12. **reporting** - Data analytics & interactive reporting

### Organizational Apps

13. **company** - Multi-tenant organization management

### Support Apps

14. **landing** - Public-facing landing pages
15. **chatbot** - Conversational AI support
16. **feedback** - Bug reporting and user feedback

## Updated Business Process Mapping

Based on Greenova-Workflow.bpmn:

1. **Authentication Flow** → `core` app (consolidated user management + auditing)
2. **Main Dashboard Interface & Navigation** → `dashboard` + `navigation` + `sidebar` apps
3. **Comprehensive Obligation Management** → `obligations` app
4. **User Role Assignment & Responsibility Management** → `responsibilities` app
5. **Project & Environmental Mechanism Management** → `projects` + `mechanisms` apps
6. **User Profile & Company Management** → `core` + `company` apps
7. **Data Analytics & Interactive Reporting** → `reporting` app
8. **Notification & Communication System** → `chatbot` app

## Data Flow (Updated)

- All apps use `protobuf` for data serialization
- `core` provides audit trails for all apps (consolidated auditing functionality)
- `company` provides organizational context for all apps
- `reporting` aggregates data from all business process apps

## Dependencies Update

All app prompts have been updated to reflect:

- **Depends on**: `core` (users, auth, audit services) instead of separate `users` and `auditing` apps
- **Navigation**: All apps include `navigation` & `sidebar` components
- **Audit Services**: All apps receive audit trail services from `core`
