# Greenova Business Scope Generation Guide

Use this prompt to generate comprehensive business scopes for new modules and
use cases within the Greenova environmental management system. The generated
content should follow the established structure and meet the technical
requirements of the Greenova project.

## Module Definition Instructions

When requesting a business scope, provide the following information:

- Module name (e.g., "Environmental Auditing", "Compliance Tracking")
- Primary purpose of the module
- Key stakeholders who will use the module
- Main business problems it solves

## Document Structure Requirements

### 1. Title and Overview

Generate a clear, concise title for the module followed by an overview
paragraph that:

- Explains the module's purpose in the context of environmental management
- Highlights its primary functions
- States its overall business value

Example:

```
# [Module Name] Module

## Overview

The Greenova [Module Name] Module provides [primary function description] for organizations to [key capability]. This module facilitates [main benefits], [secondary benefits], and [tertiary benefits].
```

### 2. Business Scope Section

Define 4-6 critical business needs addressed by the module using bullet points.
Each need should:

- Start with a bold heading (2-3 words)
- Include a brief explanation (1 sentence)

Example:

```
## Business Scope

The [module name] addresses several critical business needs:

- **Regulatory Compliance**: Ensures adherence to environmental laws, regulations, and standards
- **Risk Management**: Identifies, assesses, and mitigates environmental compliance risks
```

### 3. Key Use Cases

Describe 3-5 primary use cases for the module, each containing:

- Numbered heading with use case name
- 2-3 sentence description explaining the workflow
- Focus on user roles and system interactions

Example:

```
## Key Use Cases

### 1. Compliance Verification

Environmental managers use the [module] to verify that operations comply with relevant environmental mechanisms. The system automatically pulls obligations from the register based on selected mechanisms, creating a structured evaluation framework.
```

### 4. Process Flow

Create a Mermaid flowchart that illustrates the complete workflow, including:

- Clear start and end points
- Decision points with branches
- Status transitions
- User interaction points
- System automations

Example:

````
## Process Flow

The following flowchart illustrates the complete [module] process workflow:

```mermaid
flowchart TD
    A[Start Process] --> B[Create New Record]
    B --> C[Input Parameters]
    C --> D[Select Options]
    D --> E{Options Valid?}
    E -->|Yes| F[Next Step]
    E -->|No| G[Display Error]
    F --> H[End Process]
````

```

### 5. Data Model

Create a table showing the key data entities with columns for:
- Entity name
- Description
- Relationship to other entities

Example:
```

## Data Model

The [module name] uses the following key data entities:

| Entity | Description                | Relationship          |
| ------ | -------------------------- | --------------------- |
| Record | Top-level record (XX-XXXX) | Multiple entries      |
| Entry  | Individual item            | Belongs to one record |

```

### 6. Status Management

Define the status tracking system for the module including:
- Status values for each entity type
- Automated status transitions
- Business rules for status changes

### 7. Technical Implementation

Provide pseudocode that outlines the core functionality using:
- Functions with descriptive names
- Input and output parameters
- Business logic in plain language
- Validation rules and error handling
- Clear module organization with comments

### 8. Integration Points

List 3-5 integration points with other Greenova modules or systems.

### 9. User Interface Requirements

Outline the UI requirements focusing on user workflow and interactions.

### 10. Accessibility Considerations

Include specific accessibility considerations that ensure WCAG 2.1 AA compliance.

## Technical Constraints

The generated business scope must align with Greenova's technical stack:
- Django 4.1.13 backend with Python 3.9.21
- PicoCSS as primary frontend framework
- django-hyperscript for simple interactions
- django-htmx for AJAX functionality
- Accessible interfaces meeting WCAG 2.1 AA standards

## Output Format

Generate the final business scope document in GitHub Flavored Markdown format.
```
