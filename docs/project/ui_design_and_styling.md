## Project Business Scope Plan

### Project Title

Front-End UI Design and Styling Using PicoCSS and Django-Tailwind

### Project Overview

The goal of this project is to enhance the front-end UI design and styling of
the Greenova project using PicoCSS and Django-Tailwind. The project involves
creating a visually appealing and responsive UI using classless PicoCSS and
Django-Tailwind (Python-specific version) while avoiding the JavaScript main
version of Tailwind CSS.

### Objectives

1. Understand the current UI design and styling of the project.
2. Identify areas for improvement in the UI design and styling.
3. Implement PicoCSS for classless styling.
4. Implement Django-Tailwind for utility classes and advanced styling.
5. Ensure the UI is responsive and accessible.
6. Test the new UI design and styling to ensure it works correctly.

### Deliverables

1. A detailed analysis of the current UI design and styling.
2. A list of areas for improvement in the UI design and styling.
3. Updated code with PicoCSS and Django-Tailwind implementations.
4. Documentation explaining the changes made.
5. Test results demonstrating the functionality and responsiveness of the new
   UI design and styling.

### Timeline

- **Week 1**: Analyze the current UI design and styling and understand PicoCSS
  and Django-Tailwind.
- **Week 2**: Identify areas for improvement and create a plan.
- **Week 3**: Implement PicoCSS for classless styling.
- **Week 4**: Implement Django-Tailwind for utility classes and advanced
  styling.
- **Week 5**: Ensure the UI is responsive and accessible.
- **Week 6**: Test the new UI design and styling and document the changes.

### Tasks

#### Week 1: Analysis and Understanding

1. **Analyze Current UI Design and Styling**: Review the current UI design and
   styling to understand the existing structure and layout.
2. **Research PicoCSS and Django-Tailwind**: Learn about PicoCSS and
   Django-Tailwind, including their uses and benefits.
3. **Ask Questions**: If there are any parts of the current UI design or
   PicoCSS and Django-Tailwind that you don't understand, ask for
   clarification.

#### Week 2: Identifying Areas for Improvement

1. **Identify Areas for Improvement**: Determine which parts of the UI design
   and styling can be improved using PicoCSS and Django-Tailwind.
2. **Create a Plan**: Write down a list of improvements you plan to make and
   how you will implement them.

#### Week 3: Implementing PicoCSS for Classless Styling

1. **Update Code**: Replace existing CSS with PicoCSS for classless styling.
   Make sure to:
   - Use semantic HTML elements for styling.
   - Leverage PicoCSS's classless approach for basic styling.
   - Ensure consistency across different pages and components.

#### Week 4: Implementing Django-Tailwind for Utility Classes

1. **Set Up Django-Tailwind**: Install and configure Django-Tailwind in the
   project.
2. **Update Code**: Use Django-Tailwind utility classes for advanced styling
   and layout. Make sure to:
   - Use utility classes for spacing, typography, colors, and other styling
     properties.
   - Avoid using the JavaScript main version of Tailwind CSS.
   - Ensure compatibility with PicoCSS styling.

#### Week 5: Ensuring Responsiveness and Accessibility

1. **Responsive Design**: Ensure the UI is responsive and works well on
   different devices and screen sizes.
2. **Accessibility**: Ensure the UI meets accessibility standards. This
   includes:
   - Using proper ARIA labels and roles.
   - Ensuring keyboard navigation support.
   - Providing sufficient color contrast.

#### Week 6: Testing and Documentation

1. **Thorough Testing**: Test the new UI design and styling in different
   scenarios to ensure they work as expected.
2. **Document Changes**: Write a document explaining the changes you made.
   Include:
   - The original UI design and styling issues you identified.
   - The improvements you made using PicoCSS and Django-Tailwind.
   - How the new design and styling benefit the project.
3. **Final Review**: Review the new UI design and styling and documentation
   with your supervisor to ensure everything is correct.

### Communication Plan

- **Weekly Meetings**: Schedule a weekly meeting with your supervisor to
  discuss your progress and any challenges you are facing.
- **Daily Check-ins**: Provide daily updates on your progress via email or a
  project management tool.
- **Feedback**: Be open to feedback and make changes as necessary.

### Resources

- **PicoCSS Documentation**: Read the official PicoCSS documentation for
  reference.
- **Django-Tailwind Documentation**: Read the official Django-Tailwind
  documentation for reference.
- **Supervisor**: Reach out to your supervisor for guidance and clarification.

### Evaluation Criteria

- **Completeness**: All tasks and deliverables are completed.
- **Quality**: The new UI design and styling are visually appealing,
  responsive, and accessible.
- **Functionality**: The new design and styling work correctly in all test
  scenarios.
- **Communication**: Regular updates and effective communication with the
  supervisor.

### Example Implementation

#### Example PicoCSS Implementation

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Greenova</title>
    <link
      rel="stylesheet"
      href="https://unpkg.com/@picocss/pico@latest/css/pico.min.css"
    />
  </head>
  <body>
    <header>
      <nav>
        <ul>
          <li><a href="/">Home</a></li>
          <li><a href="/about">About</a></li>
          <li><a href="/contact">Contact</a></li>
        </ul>
      </nav>
    </header>
    <main>
      <h1>Welcome to Greenova</h1>
      <p>This is the home page of Greenova project.</p>
    </main>
    <footer>
      <p>&copy; 2025 Greenova. All rights reserved.</p>
    </footer>
  </body>
</html>
```

#### Example Django-Tailwind Implementation

1. **Install Django-Tailwind**:

   ```bash
   pip install django-tailwind
   ```

2. **Configure Django-Tailwind**: Add `tailwind` to `INSTALLED_APPS` in
   `settings.py` and create a Tailwind app:

   ```bash
   python manage.py tailwind init
   ```

3. **Use Django-Tailwind Utility Classes**:

   ```html
   <div class="container mx-auto px-4">
     <h1 class="text-2xl font-bold">Welcome to Greenova</h1>
     <p class="mt-4">This is the home page of Greenova project.</p>
   </div>
   ```

### Conclusion

Enhancing the front-end UI design and styling using PicoCSS and Django-Tailwind
is a crucial task that will improve the visual appeal and responsiveness of the
Greenova project. By following this plan, you will be able to contribute
significantly to the project's success while gaining valuable experience in
modern front-end development techniques.

Good luck with your project!

The following references were attached as context:

{"repoID":0,"ref":"","type":"repo-instructions","url":"/enssol/greenova/blob/refs/heads/main/.github/copilot-instructions.md"}

cameron Tues x 4 Thurs x 4 Fri x 4 10am to 2pm 150 hours 9 weeks all remote
Friday, April 25, 2025

## CSS Refactoring: Transitioning to SASS and PostCSS in Django

This document outlines a comprehensive plan for refactoring our current CSS
structure to utilize SASS and PostCSS, improving our styling workflow while
maintaining compatibility with our Django project.

### Current Structure

Our current CSS is organized in a logical directory structure:

```plaintext
/static/css/
├── main.css                  # Main entry point
├── base/                     # Fundamental styles
├── abstracts/                # Reusable code with no direct output
├── themes/                   # Theme-specific styles
├── components/               # Reusable interface components
├── features/                 # Feature-specific styles
├── utils/                    # Utility classes
└── vendor/                   # Third-party CSS
```

### Benefits of SASS and PostCSS Integration

1. **Enhanced Maintainability**: Variables, mixins, and nesting for cleaner
   code
2. **Improved Performance**: Optimized and minified output via PostCSS
3. **Future-Proof CSS**: Use modern features with automatic browser
   compatibility
4. **Better Development Experience**: Live reloading, error reporting, and
   modular imports

### Implementation Plan

#### 1. Setup and Installation

```bash
# Create package.json if not exists
npm init -y

# Install core dependencies
npm install --save-dev sass postcss postcss-cli autoprefixer cssnano postcss-preset-env

# Install additional useful PostCSS plugins
npm install --save-dev postcss-import postcss-mixins postcss-nested postcss-custom-properties

# Optional development tools
npm install --save-dev npm-run-all onchange
```

#### 2. File Structure Conversion

Convert the existing CSS directory structure to accommodate SASS:

```plaintext
/static/
├── scss/                      # Source SASS files
│   ├── main.scss              # Main entry point
│   ├── base/
│   │   ├── _reset.scss        # Underscore prefix for partials
│   │   ├── _typography.scss
│   │   ├── _layout.scss
│   │   └── _accessibility.scss
│   ├── abstracts/
│   │   ├── _variables.scss
│   │   ├── _mixins.scss
│   │   └── _functions.scss
│   ├── themes/
│   │   ├── _theme-variables.scss
│   │   ├── _light.scss
│   │   └── _dark.scss
│   ├── components/            # Component styles with .scss extension
│   ├── features/              # Feature-specific styles
│   ├── utils/                 # Utility classes
│   └── vendor/                # Third-party styles
├── css/                       # Compiled output directory
│   └── main.css               # Final compiled and optimized CSS
```

#### 3. Configuration Files

**PostCSS Configuration**:

```js
// postcss.config.js
module.exports = {
  plugins: [
    // Process @import statements
    require('postcss-import'),

    // Enable custom mixins and nesting (similar to SASS)
    require('postcss-mixins'),
    require('postcss-nested'),

    // Process CSS variables
    require('postcss-custom-properties'),

    // Use modern CSS features with browser compatibility
    require('postcss-preset-env')({
      stage: 1,
      browsers: ['> 1%', 'last 2 versions', 'not dead'],
    }),

    // Add vendor prefixes
    require('autoprefixer'),

    // Minify CSS for production only
    process.env.NODE_ENV === 'production'
      ? require('cssnano')({ preset: 'default' })
      : null,
  ].filter(Boolean), // Remove null plugins
};
```

**NPM Scripts**:

```json
"scripts": {
  "sass": "sass --no-source-map static/scss/main.scss:static/css/.temp/main.css",
  "postcss": "postcss static/css/.temp/main.css -o static/css/main.css",
  "build": "npm run sass && npm run postcss",
  "watch": "npm-run-all --parallel watch:*",
  "watch:sass": "sass --watch static/scss/main.scss:static/css/.temp/main.css",
  "watch:postcss": "onchange 'static/css/.temp/*.css' -- npm run postcss"
}
```

#### 4. Main SASS Entry File

Create a main.scss file that imports all partials:

```scss
// Base
@import 'base/reset';
@import 'base/typography';
@import 'base/layout';
@import 'base/accessibility';

// Abstracts
@import 'abstracts/variables';
@import 'abstracts/mixins';
@import 'abstracts/functions';

// Themes
@import 'themes/theme-variables';
@import 'themes/light';
@import 'themes/dark';

// Components - import all component partials
@import 'components/buttons/base';
@import 'components/buttons/primary';
@import 'components/buttons/action';
// Other component imports

// Features
@import 'features/obligations/index';
@import 'features/user-profile/index';
@import 'features/company/index';

// Utils
@import 'utils/spacing';
@import 'utils/display';
@import 'utils/colors';

// Vendor - For non-NPM vendor files
@import 'vendor/pico/pico-classless';
```

#### 5. Django Integration

**Django Settings Configuration**:

```python
# settings.py
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# For production
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

**Custom Django Management Command**:

```python
# yourapp/management/commands/build_sass.py
from django.core.management.base import BaseCommand
import subprocess
import os

class Command(BaseCommand):
    help = 'Build SASS files to CSS with PostCSS processing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--production',
            action='store_true',
            help='Build for production environment',
        )

    def handle(self, *args, **options):
        self.stdout.write('Building frontend assets...')

        env = os.environ.copy()
        if options['production']:
            env['NODE_ENV'] = 'production'

        subprocess.run(['npm', 'run', 'build'], env=env, check=True)
        self.stdout.write(self.style.SUCCESS('CSS build complete!'))
```

### Leveraging SASS Features

#### Variables and Custom Properties

```scss
// abstracts/_variables.scss
$spacing-base: 0.5rem;
$spacing-small: $spacing-base * 0.5;
$spacing-large: $spacing-base * 1.5;

:root {
  --greenova-spacing: #{$spacing-base};
  --greenova-spacing-small: #{$spacing-small};
  --greenova-spacing-large: #{$spacing-large};
}
```

#### Mixins for Responsive Design

```scss
// abstracts/_mixins.scss
@mixin respond-to($breakpoint) {
  @if $breakpoint == 'small' {
    @media (max-width: 576px) {
      @content;
    }
  } @else if $breakpoint == 'medium' {
    @media (max-width: 768px) {
      @content;
    }
  } @else if $breakpoint == 'large' {
    @media (max-width: 992px) {
      @content;
    }
  } @else if $breakpoint == 'xlarge' {
    @media (max-width: 1200px) {
      @content;
    }
  }
}

// Usage
.card-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);

  @include respond-to(medium) {
    grid-template-columns: repeat(2, 1fr);
  }

  @include respond-to(small) {
    grid-template-columns: 1fr;
  }
}
```

#### Component Example with SASS Features

```scss
// components/buttons/_base.scss
@mixin button-base {
  font-size: var(--greenova-button-size);
  font-weight: bold;
  min-height: 41px;
  border-radius: var(--greenova-border-radius);
  padding: var(--greenova-padding);
  cursor: pointer;
  transition: background-color 0.2s;
  &:hover {
    background-color: var(--greenova-green-tertiary);
    border-color: var(--greenova-green-tertiary);
  }
}

button,
[type='submit'],
[type='reset'],
.btn-primary,
.btn-secondary,
.btn-danger,
.action-btn {
  @include button-base;
}
```

### Leveraging PostCSS Features

#### Using PostCSS Nesting

```css
/* For components that don't need SASS complexity */
.data-card {
  padding: var(--spacing-medium);

  /* Nesting via PostCSS */
  & .card-header {
    border-bottom: 1px solid var(--border-color);

    & h3 {
      margin-bottom: 0;
    }
  }
}
```

#### Using Modern CSS Features via PostCSS

```css
/* Using logical properties (handled by postcss-preset-env) */
.section {
  margin-inline: auto;
  padding-block: var(--spacing-large);
}

/* Using focus-visible for better keyboard navigation */
.button:focus-visible {
  outline: 2px solid var(--greenova-focus-color);
  outline-offset: 2px;
}
```

### Migration Strategy

1. **Incremental Approach**:

   - Start by converting one component category (e.g., buttons)
   - Test thoroughly before moving to the next component
   - Maintain backward compatibility during transition

2. **Create a Base Foundation**:

   - Set up variables and mixins first
   - Convert global styles next
   - Then move to specific components

3. **Documentation**:

   - Document conversion decisions
   - Create style guides for new components
   - Update team documentation

4. **Integration with Build Process**:
   - Add to CI/CD pipeline
   - Include in deployment workflow
   - Ensure both development and production builds work

### Resources

- [SASS Documentation](https://sass-lang.com)
- [PostCSS Documentation](https://postcss.org)
- [Django Static Files](https://docs.djangoproject.com/en/stable/howto/static-files/)
