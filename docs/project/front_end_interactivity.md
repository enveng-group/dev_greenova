## Project Business Scope Plan

### Project Title

Enhancing Front-End Interactivity Using Django-HTMX and Django-Hyperscript

### Project Overview

The goal of this project is to enhance the front-end interactivity of the Greenova project using Django-HTMX and Django-Hyperscript. The project aims to remove all JavaScript implementations and replace them with Python implementations using Django-HTMX and Django-Hyperscript, along with Django and Python standard library implementations.

### Objectives

1. Understand the current JavaScript implementations for front-end interactivity.
2. Identify areas where Django-HTMX and Django-Hyperscript can replace JavaScript.
3. Implement Django-HTMX and Django-Hyperscript to enhance front-end interactivity.
4. Ensure all JavaScript code is removed and replaced with Python implementations.
5. Test the new implementations to ensure they work correctly.

### Deliverables

1. A detailed analysis of the current JavaScript implementations.
2. A list of areas where Django-HTMX and Django-Hyperscript can be used.
3. Updated code with Django-HTMX and Django-Hyperscript implementations.
4. Documentation explaining the changes made.
5. Test results demonstrating the functionality of the new implementations.

### Timeline

- **Week 1**: Analyze current JavaScript implementations and understand Django-HTMX and Django-Hyperscript.
- **Week 2**: Identify areas for replacement and create a plan.
- **Week 3**: Implement Django-HTMX and Django-Hyperscript for identified areas.
- **Week 4**: Test the new implementations and document the changes.

### Tasks

#### Week 1: Analysis and Understanding

1. **Analyze JavaScript Implementations**: Review the current JavaScript code to understand how front-end interactivity is achieved.
2. **Research Django-HTMX and Django-Hyperscript**: Learn about Django-HTMX and Django-Hyperscript, including their uses and benefits.
3. **Ask Questions**: If there are any parts of the JavaScript code or Django-HTMX and Django-Hyperscript that you don't understand, ask for clarification.

#### Week 2: Identifying Areas for Replacement

1. **Identify Areas for Replacement**: Determine which JavaScript functionalities can be replaced with Django-HTMX and Django-Hyperscript.
2. **Create a Plan**: Write down a list of replacements you plan to make and how you will implement them.

#### Week 3: Implementing Changes

1. **Update Code**: Replace JavaScript implementations with Django-HTMX and Django-Hyperscript. Make sure to:
   - Use Django-HTMX for AJAX requests and dynamic content loading.
   - Use Django-Hyperscript for client-side interactivity.
   - Ensure all interactions are handled using Django and Python standard library implementations.
2. **Test Regularly**: After making each change, test the new implementation to ensure it works correctly.

#### Week 4: Testing and Documentation

1. **Thorough Testing**: Test the new implementations in different scenarios to ensure they work as expected.
2. **Document Changes**: Write a document explaining the changes you made. Include:
   - The original JavaScript functionalities you identified.
   - The replacements you made using Django-HTMX and Django-Hyperscript.
   - How the new implementations benefit the project.
3. **Final Review**: Review the new implementations and documentation with your supervisor to ensure everything is correct.

### Communication Plan

- **Weekly Meetings**: Schedule a weekly meeting with your supervisor to discuss your progress and any challenges you are facing.
- **Daily Check-ins**: Provide daily updates on your progress via email or a project management tool.
- **Feedback**: Be open to feedback and make changes as necessary.

### Resources

- **Django-HTMX Documentation**: Read the official Django-HTMX documentation for reference.
- **Django-Hyperscript Documentation**: Read the official Django-Hyperscript documentation for reference.
- **Supervisor**: Reach out to your supervisor for guidance and clarification.

### Evaluation Criteria

- **Completeness**: All tasks and deliverables are completed.
- **Quality**: The new implementations are efficient, readable, and well-documented.
- **Functionality**: The new implementations work correctly in all test scenarios.
- **Communication**: Regular updates and effective communication with the supervisor.

### Suggested Improvements and Recommendations

#### Replacing JavaScript with Django-HTMX and Django-Hyperscript

1. **AJAX Requests**: Use Django-HTMX for making AJAX requests and updating content dynamically.

   - Example:

     ```html
     <div
       hx-get="/some-endpoint/"
       hx-trigger="click"
       hx-target="#content"
     ></div>
     ```

2. **Client-Side Interactivity**: Use Django-Hyperscript for handling client-side interactivity.

   - Example:

     ```html
     <button type="button" _="on click toggle .hidden on #details">
       Toggle Details
     </button>
     <div id="details" class="hidden">...</div>
     ```

3. **Form Submissions**: Use Django-HTMX to handle form submissions and validation.

   - Example:

     ```html
     <form hx-post="/submit-form/" hx-target="#result">
       {% csrf_token %}
       <input type="text" name="name" required />
       <button type="submit">Submit</button>
     </form>
     <div id="result"></div>
     ```

4. **Progressive Enhancement**: Ensure base functionality works without JavaScript, and enhance it with Django-HTMX and Django-Hyperscript.

   - Example:

     ```html
     <!-- Base functionality -->
     <form method="post" action="/submit">
       {% csrf_token %}
       <input type="text" name="name" required />
       <button type="submit">Submit</button>
     </form>

     <!-- Enhanced functionality -->
     <form hx-post="/submit/" hx-target="#result">
       {% csrf_token %}
       <input type="text" name="name" required />
       <button type="submit">Submit</button>
     </form>
     <div id="result"></div>
     ```

### Conclusion

Enhancing the front-end interactivity using Django-HTMX and Django-Hyperscript is a crucial task that will streamline the development process and improve user experience. By following this plan, you will be able to contribute significantly to the project's success while gaining valuable experience in Django and modern web development techniques.

Good luck with your project!

The following references were attached as context:

{"repoID":0,"ref":"","type":"repo-instructions","url":"/enssol/greenova/blob/refs/heads/main/.github/copilot-instructions.md"}

jared

100 hours

8 hours a week

Wednesday and Thursday 10am to 2pm

give or take last week of May 23rd

<@358385377645428737> here is more context with modularising javascript and transitioning to Typescript:

JavaScript/TypeScript Directory Structure Recommendations for Django
Based on reviewing your JavaScript files, here's a recommended structure to make your scripts more modular and easier to maintain, along with guidance for transitioning to TypeScript.

Recommended Directory Structure

```plaintext
/static/js/
├── main.js                    # Main entry point that imports and initializes all modules
├── core/                      # Core application functionality
│   ├── config.js              # Configuration parameters and constants
│   ├── events.js              # Global event handling
│   ├── utils.js               # Common utility functions
│   └── api.js                 # API interaction helpers
│
├── components/                # Reusable UI components
│   ├── charts/                # Chart-related functionality
│   │   ├── chart-scroll.js    # Chart scrolling implementation
│   │   └── chart-loader.js    # Chart initialization and data handling
│   ├── tables/                # Table handling
│   │   ├── table-scroll.js    # Table scrolling functionality
│   │   └── table-export.js    # Table export features
│   ├── navigation.js          # Navigation functionality
│   ├── theme-switcher.js      # Theme switching functionality
│   ├── form-handlers.js       # Form submission and validation
│   └── modals.js              # Modal dialog functionality
│
├── features/                  # Feature-specific code
│   ├── obligations/           # Obligation-specific functionality
│   │   ├── index.js           # Main obligations module
│   │   ├── filters.js         # Obligation filtering
│   │   └── status-updates.js  # Obligation status functionality
│   ├── projects/              # Project-related functionality
│   │   ├── index.js           # Main project module
│   │   └── selector.js        # Project selection
│   └── user-profile/          # User profile functionality
│
├── lib/                       # Internal libraries and wrappers
│   ├── htmx-wrapper.js        # HTMX integration helpers
│   └── hyperscript-helpers.js # Hyperscript integration helpers
│
├── vendor/                    # Third-party libraries
│   ├── htmx/                  # HTMX library and extensions
│   │   ├── htmx.min.js
│   │   └── ext/               # HTMX extensions
│   │       ├── path-deps.min.js
│   │       ├── loading-states.min.js
│   │       ├── head-support.min.js
│   │       └── class-tools.min.js
│   └── hyperscript/           # Hyperscript library
│       └── _hyperscript.min.js
│
└── types/                     # TypeScript type definitions (for TS transition)
    ├── global.d.ts            # Global type definitions
    ├── htmx.d.ts              # Type definitions for HTMX
    └── hyperscript.d.ts       # Type definitions for Hyperscript
```

Key Benefits of This Structure
Improved Separation of Concerns:

Core application logic separated from UI components
Feature-specific code isolated in its own directory
Clear boundaries between application code and vendor scripts
Better Maintainability:

Smaller, more focused files
Logical grouping of related functionality
Easier to locate and modify specific features
Simplified Dependency Management:

Clear import paths
Centralized vendor script management
Better control over script loading order
Enhanced Team Collaboration:

Multiple developers can work on different components without conflicts
Clear ownership of code modules
Consistent structure across the project
TypeScript Migration Guidance

1. Initial Setup
   Add TypeScript to your Django project:

```bash
# Install TypeScript and types for libraries
npm install --save-dev typescript @types/node
# For your libraries (if available)
npm install --save-dev @types/htmx
```

Create a tsconfig.json at project root:

```json
{
  "compilerOptions": {
    "target": "ES2015",
    "module": "ES2015",
    "moduleResolution": "node",
    "esModuleInterop": true,
    "strict": true,
    "outDir": "./greenova/static/js/dist",
    "rootDir": "./typescript",
    "sourceMap": true,
    "declaration": false,
    "baseUrl": "./",
    "paths": {
      "@core/*": ["typescript/core/*"],
      "@components/*": ["typescript/components/*"],
      "@features/*": ["typescript/features/*"],
      "@lib/*": ["typescript/lib/*"]
    }
  },
  "include": ["typescript/**/*.ts"],
  "exclude": ["node_modules"]
}
```

2. Phased Migration Strategy
   Setup TypeScript Source Directory:

Create a /typescript directory at project root with the same structure as /static/js/
Configure Django to serve compiled JavaScript from /static/js/dist/
Start with Type Definitions:

Create type definitions for existing JavaScript modules
Add TypeScript interfaces for your data structures and API responses
Incremental Module Migration:

Start with independent utilities and smaller components
Rename .js files to .ts files and add type annotations
Address TypeScript errors as they appear
Implement proper interfaces for function parameters and return types
Configure Build Process:

Add npm scripts for TypeScript compilation
Set up watch mode for development
Add integration with Django's static file collection 3. Django Integration
Update your Django templates to include the compiled JavaScript:

```html
{% load static %}
<script src="{% static 'js/dist/main.js' %}"></script>
```

Set up a build script in package.json:

```json
{
  "scripts": {
    "build": "tsc",
    "watch": "tsc --watch",
    "prebuild": "rimraf ./greenova/static/js/dist",
    "django-collect": "npm run build && python manage.py collectstatic --noinput"
  }
}
```

4. Webpack Integration (Optional)
   For a more robust build system, consider adding Webpack:

```sh
npm install --save-dev webpack webpack-cli ts-loader
```

Create a webpack.config.js:

```js
const path = require('path');

module.exports = {
  entry: './typescript/main.ts',
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        use: 'ts-loader',
        exclude: /node_modules/,
      },
    ],
  },
  resolve: {
    extensions: ['.tsx', '.ts', '.js'],
    alias: {
      '@core': path.resolve(__dirname, 'typescript/core/'),
      '@components': path.resolve(__dirname, 'typescript/components/'),
      '@features': path.resolve(__dirname, 'typescript/features/'),
      '@lib': path.resolve(__dirname, 'typescript/lib/'),
    },
  },
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'greenova/static/js/dist'),
  },
};
```

5. Tips for TypeScript Migration
   Start with strict mode disabled and gradually enable it as codebase matures
   Create proper interfaces for your Django API responses
   Use enums for constants that are currently defined as strings
   Add event typing for all event handlers
   Create utility types for common patterns in your application
   Document public APIs with JSDoc comments for better IDE support
   This structure and migration plan will help organize your JavaScript code better while providing a clear path to TypeScript adoption, improving maintainability and type safety in your Django project.
