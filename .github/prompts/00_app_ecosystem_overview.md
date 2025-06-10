<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Greenova App Ecosystem and Business Process Workflow](#greenova-app-ecosystem-and-business-process-workflow)
  - [Overview](#overview)
  - [Business Process Flow Summary](#business-process-flow-summary)
  - [Enhanced User Journey Details](#enhanced-user-journey-details)
  - [App Dependencies and Relationships](#app-dependencies-and-relationships)
    - [Core Foundation Apps](#core-foundation-apps)
      - [1. `core` App](#1-core-app)
      - [2. `navigation` App](#2-navigation-app)
      - [3. `sidebar` App](#3-sidebar-app)
      - [4. `protobuf` App](#4-protobuf-app)
    - [Business Process Apps](#business-process-apps)
      - [5. `dashboard` App](#5-dashboard-app)
      - [6. `obligations` App](#6-obligations-app)
      - [7. `projects` App](#7-projects-app)
      - [8. `mechanisms` App](#8-mechanisms-app)
      - [9. `responsibilities` App](#9-responsibilities-app)
      - [10. `audits` App](#10-audits-app)
      - [11. `procedures` App](#11-procedures-app)
      - [12. `reporting` App](#12-reporting-app)
    - [Organizational Apps](#organizational-apps)
      - [13. `company` App](#13-company-app)
    - [Support Apps](#support-apps)
      - [14. `landing` App](#14-landing-app)
      - [15. `chatbot` App](#15-chatbot-app)
      - [16. `feedback` App](#16-feedback-app)
  - [Summary](#summary)
    - [Foundation (4 apps)](#foundation-4-apps)
    - [Business Process (8 apps)](#business-process-8-apps)
    - [Organizational (1 app)](#organizational-1-app)
    - [Support (3 apps)](#support-3-apps)
  - [Inter-App Communication Patterns](#inter-app-communication-patterns)
    - [Data Flow](#data-flow)
    - [UI/UX Flow](#uiux-flow)
    - [Security Flow](#security-flow)
      - [16. `feedback` App](#16-feedback-app-1)
  - [User Journey Flow](#user-journey-flow)
  - [Cross-Cutting Concerns](#cross-cutting-concerns)
    - [Data Flow](#data-flow-1)
    - [UI Consistency](#ui-consistency)
    - [Security & Permissions](#security--permissions)
    - [Notification System](#notification-system)
  - [Final App Count and Structure](#final-app-count-and-structure)
    - [Foundation Layer (4 apps)](#foundation-layer-4-apps)
    - [Business Process Layer (8 apps)](#business-process-layer-8-apps)
    - [Organizational Layer (1 app)](#organizational-layer-1-app)
    - [Support Layer (3 apps)](#support-layer-3-apps)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Greenova App Ecosystem and Business Process Workflow

## Overview

This document outlines the complete app ecosystem for the Greenova Environmental Management System and how each app contributes to the overall business process workflow as defined in Greenova-Workflow.bpmn.

## Business Process Flow Summary

Based on the Greenova-Workflow.bpmn, the system implements these core business processes:

1. **Authentication Flow** - User login, registration, email verification, and access control with detailed user decision points
2. **Main Dashboard Interface & Navigation** - Central hub for system navigation with explicit user selection gateways and decision flows
3. **Comprehensive Obligation Management** - Core environmental obligation tracking
4. **User Role Assignment & Responsibility Management** - Accountability and ownership
5. **Project & Environmental Mechanism Management** - Implementation coordination
6. **User Profile & Company Management** - Organization and user context
7. **Data Analytics & Interactive Reporting** - Performance insights and compliance
8. **Notification & Communication System** - Automated alerts and updates

## Enhanced User Journey Details

The updated BPMN includes detailed user decision points with explicit gateways for:

- **Project Selection Logic**: "Is Project Selected?" gateway with paths for selection, cancellation, and prompting
- **Mechanism Selection Logic**: "Is Mechanism Selected?" gateway with decision branches
- **Procedure Selection Logic**: "Is Procedure Selected?" gateway with user action flows
- **Obligation Selection Logic**: "Is Obligation Selected?" gateway with drill-down navigation
- **Error Handling**: Multiple end events for authentication failures, verification timeouts
- **Timer Events**: 24-hour email verification timeout with boundary events
- **Retry Logic**: Explicit loops for login retry attempts and user navigation flows

## App Dependencies and Relationships

### Core Foundation Apps

#### 1. `core` App

- **Business Process**: Authentication Flow + User Profile Management + Audit Trail Management
- **Purpose**: Foundation app providing authentication, user management, auditing, base templates, and shared utilities
- **Dependencies**: None (foundation)
- **Serves**: All other apps
- **Key Functions**: User authentication, user profiles, comprehensive audit trails, base templates, shared utilities, django-allauth integration

#### 2. `navigation` App

- **Business Process**: Supporting Infrastructure
- **Purpose**: Centralized navigation UI components
- **Dependencies**: `core` (base templates)
- **Serves**: All apps requiring navigation
- **Key Functions**: Navigation bars, menus, breadcrumbs

#### 3. `sidebar` App

- **Business Process**: Supporting Infrastructure
- **Purpose**: Centralized sidebar UI components
- **Dependencies**: `core` (base templates)
- **Serves**: All apps requiring sidebar functionality
- **Key Functions**: Sidebar widgets, quick links, contextual information

#### 4. `protobuf` App

- **Business Process**: Supporting Infrastructure
- **Purpose**: Centralized Protocol Buffer schema management
- **Dependencies**: None
- **Serves**: All apps requiring data serialization
- **Key Functions**: Proto file management, stub generation

### Business Process Apps

#### 5. `dashboard` App

- **Business Process**: Main Dashboard Interface & Navigation
- **Purpose**: Central hub for navigation and overview
- **Dependencies**: `core`, `navigation`, `sidebar`, `company`
- **Integrates with**: All data apps for summaries
- **Key Functions**: Data aggregation, navigation gateway, context management

#### 6. `obligations` App

- **Business Process**: Comprehensive Obligation Management
- **Purpose**: Core environmental obligation tracking and compliance
- **Dependencies**: `core`, `navigation`, `sidebar`, `company`
- **Integrates with**: `projects`, `responsibilities`, `mechanisms`, `audits`, `auditing`
- **Serves**: `dashboard`, `reporting`
- **Key Functions**: Obligation CRUD, compliance tracking, evidence management, automated reminders

#### 7. `projects` App

- **Business Process**: Project & Environmental Mechanism Management
- **Purpose**: Environmental project coordination and delivery
- **Dependencies**: `core`, `navigation`, `sidebar`, `company`
- **Integrates with**: `obligations`, `mechanisms`, `responsibilities`, `audits`
- **Serves**: `dashboard`, `reporting`
- **Key Functions**: Project management, resource coordination, progress tracking

#### 8. `mechanisms` App

- **Business Process**: Project & Environmental Mechanism Management
- **Purpose**: Environmental control measures and mechanisms
- **Dependencies**: `core`, `navigation`, `sidebar`, `company`
- **Integrates with**: `obligations`, `projects`, `audits`
- **Serves**: `dashboard`, `reporting`
- **Key Functions**: Mechanism management, effectiveness tracking, implementation support

#### 9. `responsibilities` App

- **Business Process**: User Role Assignment & Responsibility Management
- **Purpose**: Accountability and task assignment
- **Dependencies**: `core`, `navigation`, `sidebar`, `company`
- **Integrates with**: `obligations`, `projects`, `audits`, `mechanisms`
- **Serves**: `dashboard`, `reporting`
- **Key Functions**: Responsibility assignment, role management, accountability tracking

#### 10. `audits` App

- **Business Process**: Analytics Reporting + Compliance Verification
- **Purpose**: Specific audit events and compliance verification
- **Dependencies**: `core`, `navigation`, `sidebar`, `company`
- **Integrates with**: `obligations`, `projects`, `mechanisms`, `responsibilities`
- **Serves**: `dashboard`, `reporting`
- **Key Functions**: Audit management, findings tracking, corrective actions

#### 11. `procedures` App

- **Business Process**: Supporting all processes with standardized procedures
- **Purpose**: Standard operating procedures and documentation
- **Dependencies**: `core`, `navigation`, `sidebar`, `company`
- **Integrates with**: `obligations`, `projects`, `mechanisms`, `audits`
- **Serves**: All apps requiring procedural guidance
- **Key Functions**: SOP management, procedural documentation, workflow support

#### 12. `reporting` App

- **Business Process**: Data Analytics & Interactive Reporting
- **Purpose**: Comprehensive reporting and analytics
- **Dependencies**: `core`, `navigation`, `sidebar`, `company`
- **Integrates with**: All data apps for report generation
- **Serves**: Stakeholders, dashboard summaries
- **Key Functions**: Report generation, data visualization, performance monitoring

### Organizational Apps

#### 13. `company` App

- **Business Process**: User Profile & Company Management
- **Purpose**: Multi-tenant organization management
- **Dependencies**: `core`, `navigation`, `sidebar`
- **Integrates with**: All apps for organizational context
- **Serves**: All apps requiring company context
- **Key Functions**: Company profiles, membership management, context switching

### Support Apps

#### 14. `landing` App

- **Business Process**: Public Interface
- **Purpose**: Public-facing landing pages
- **Dependencies**: `core`, `navigation`
- **Serves**: Public users and marketing
- **Key Functions**: Landing pages, public information

#### 15. `chatbot` App

- **Business Process**: Notification & Communication System
- **Purpose**: Conversational AI and automated communication
- **Dependencies**: `core`, `navigation`, `sidebar`, `company`
- **Integrates with**: All apps for context-aware assistance
- **Serves**: Users with guided assistance and automated notifications
- **Key Functions**: Chat interface, AI assistance, automated notifications

#### 16. `feedback` App

- **Business Process**: Supporting Infrastructure
- **Purpose**: Bug reporting and user feedback management
- **Dependencies**: `core`, `navigation`, `sidebar`, `company`
- **Integrates with**: All apps for feedback collection
- **Serves**: Development team and system improvement
- **Key Functions**: Bug reports, feature requests, user feedback tracking

## Summary

The Greenova app ecosystem consists of **16 active apps** organized into four categories:

### Foundation (4 apps)

- `core`, `navigation`, `sidebar`, `protobuf`

### Business Process (8 apps)

- `dashboard`, `obligations`, `projects`, `mechanisms`, `responsibilities`, `audits`, `procedures`, `reporting`

### Organizational (1 app)

- `company`

### Support (3 apps)

- `landing`, `chatbot`, `feedback`

**Note**: The `users` and `auditing` apps have been consolidated into the `core` app to provide centralized user management and audit trail services for all applications.

## Inter-App Communication Patterns

### Data Flow

- All apps use `protobuf` for data serialization
- `core` provides audit trails for all apps (consolidated auditing functionality)
- `company` provides organizational context for all apps
- `reporting` aggregates data from all business process apps

### UI/UX Flow

- `core` provides base templates and authentication
- `navigation` and `sidebar` provide consistent UI components
- `dashboard` serves as the central navigation hub
- All business process apps integrate seamlessly through shared components

### Security Flow

- `core` handles all authentication and authorization
- `company` manages multi-tenant access control
- All apps inherit security context from `core` services
- **Business Process**: Notification & Communication System
- **Purpose**: Conversational AI support
- **Dependencies**: `core`, `navigation`, `sidebar`, `company`
- **Integrates with**: All apps for contextual assistance
- **Key Functions**: Chat support, AI assistance, user guidance

#### 16. `feedback` App

- **Business Process**: Supporting Infrastructure
- **Purpose**: Bug reporting and user feedback
- **Dependencies**: `core`, `navigation`, `sidebar`, `company`
- **Serves**: Development team and system improvement
- **Key Functions**: Bug tracking, feedback collection, issue management

## User Journey Flow

1. **Authentication** (`core`) → User logs in/registers
2. **Dashboard** (`dashboard`) → User views overview and navigates to specific functions
3. **Obligation Management** (`obligations`) → User creates/manages environmental obligations
4. **Responsibility Assignment** (`responsibilities`) → User assigns obligations to team members
5. **Project Coordination** (`projects`) → User creates projects to deliver obligations
6. **Mechanism Implementation** (`mechanisms`) → User implements control measures
7. **Compliance Verification** (`audits`) → User conducts audits and tracks compliance
8. **Reporting & Analytics** (`reporting`) → User generates reports and analyzes performance
9. **Company Management** (`company`) → User manages organization and profiles

## Cross-Cutting Concerns

### Data Flow

- All apps use `protobuf` for data serialization
- `core` provides audit trails for all apps (consolidated auditing functionality)
- `company` provides organizational context for all apps
- `reporting` aggregates data from all business process apps

### UI Consistency

- All apps extend templates from `core`
- All apps include navigation from `navigation`
- All apps include sidebar from `sidebar`
- All apps use `django-bootstrap5` for styling

### Security & Permissions

- All apps depend on `core` for authentication
- `company` app provides organizational boundaries
- `responsibilities` app manages access control
- Object-level permissions via `django-guardian`

### Notification System

- `obligations` sends compliance reminders
- `projects` sends milestone notifications
- `audits` sends audit notifications
- `chatbot` provides interactive notifications
- All apps can trigger notifications through the centralized system

This comprehensive ecosystem ensures that all business processes from the Greenova-Workflow.bpmn are properly implemented with clear separation of concerns, proper dependencies, and seamless integration across the entire system.

## Final App Count and Structure

**Total Apps: 16** (down from 18 after consolidation)

### Foundation Layer (4 apps)

- `core` - Authentication, user management, audit trails, base templates
- `navigation` - Navigation UI components
- `sidebar` - Sidebar UI components
- `protobuf` - Protocol Buffer schema management

### Business Process Layer (8 apps)

- `dashboard` - Main dashboard and navigation hub
- `obligations` - Environmental obligation management
- `projects` - Project coordination and delivery
- `mechanisms` - Environmental control measures
- `responsibilities` - Role and accountability management
- `audits` - Compliance verification and audit events
- `procedures` - Standard operating procedures
- `reporting` - Analytics and performance reporting

### Organizational Layer (1 app)

- `company` - Multi-tenant organization management

### Support Layer (3 apps)

- `landing` - Public-facing pages
- `chatbot` - AI assistance and notifications
- `feedback` - Bug reporting and system improvement

This streamlined structure eliminates redundancy while ensuring comprehensive coverage of all business processes defined in the Greenova-Workflow.bpmn.
