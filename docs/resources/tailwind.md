# Django Tailwind: The Utility-First CSS Framework for Django

## Introduction

[Tailwind CSS](https://tailwindcss.com/) is a utility-first CSS framework that provides low-level utility classes to build custom designs without leaving your HTML. [Django Tailwind](https://github.com/timonweb/django-tailwind) is a Django app that integrates Tailwind CSS into your Django project.

> **Note:** According to our coding guidelines, we should use Django Tailwind only as a last resort after semantic HTML and PicoCSS, prioritizing progressive enhancement.

## Why Consider Tailwind CSS in Django?

- **Rapid UI Development**: Build custom interfaces quickly without writing custom CSS
- **Consistent Design System**: Enforces design constraints with predefined values
- **Responsive Design**: Built-in responsive modifiers like `md:`, `lg:`, etc.
- **Dark Mode**: Simple implementation with `dark:` variants
- **Smaller Production CSS**: Generates only the CSS you use

## Installation

### 1. Install Django Tailwind package

```bash
pip install django-tailwind==3.6.0
```

### 2. Add to INSTALLED_APPS

```python
INSTALLED_APPS = [
    # ...
    'tailwind',
    # ...
]
```

### 3. Create a Tailwind CSS application

```bash
python manage.py tailwind init
```

This will prompt you to name your Tailwind app. The common choice is 'theme'.

### 4. Add your tailwind app to INSTALLED_APPS

```python
INSTALLED_APPS = [
    # ...
    'tailwind',
    'theme',  # your tailwind app
    # ...
]
```

### 5. Configure settings.py

```python
# settings.py
TAILWIND_APP_NAME = 'theme'

# For development:
INTERNAL_IPS = [
    "127.0.0.1",
]

# For production:
TAILWIND_CSS_PATH = 'css/dist/styles.css'  # the path where the compiled CSS is located
```

### 6. Install Tailwind CSS dependencies

```bash
python manage.py tailwind install
```

## Development Workflow

### 1. Start the Tailwind CSS development server

```bash
python manage.py tailwind start
```

This will watch your template files and automatically rebuild your CSS when changes are detected.

### 2. Include Tailwind CSS in your base template

```html
{% load tailwind_tags %}
<!DOCTYPE html>
<html lang="en">
<head>
    <!-- ... -->
    {% tailwind_css %}
    <!-- ... -->
</head>
<body>
    <!-- ... -->
</body>
</html>
```

### 3. Build for production

```bash
python manage.py tailwind build
```

This creates an optimized production build.

## Using Tailwind CSS Classes

Remember to follow our HTML-first approach. Only use Tailwind CSS utilities when absolutely necessary, and always maintain semantic HTML structure.

### Basic Typography

```html
<h1 class="text-3xl font-bold text-gray-900">Large Heading</h1>
<p class="text-base text-gray-700 leading-relaxed">
  This is a paragraph with normal text size and slightly relaxed line height.
</p>
```

### Layout and Spacing

```html
<main class="container mx-auto px-4 py-8">
  <section class="mb-8">
    <h2 class="text-2xl mb-4">Section Title</h2>
    <!-- Content -->
  </section>
</main>
```

### Responsive Design

```html
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  <div class="p-4 bg-white shadow rounded">Item 1</div>
  <div class="p-4 bg-white shadow rounded">Item 2</div>
  <div class="p-4 bg-white shadow rounded">Item 3</div>
</div>
```

## Customizing Tailwind

### 1. Modify the tailwind.config.js file

```javascript
// theme/static_src/tailwind.config.js
module.exports = {
  content: [
    // Templates within theme app
    '../templates/**/*.html',
    // Templates in other apps
    '../../templates/**/*.html',
    '../../**/templates/**/*.html',
  ],
  theme: {
    extend: {
      colors: {
        'brand-primary': '#1a73e8',
        'brand-secondary': '#34a853',
      },
      spacing: {
        '72': '18rem',
        '84': '21rem',
        '96': '24rem',
      },
    },
  },
  plugins: [],
}
```

### 2. Add custom utilities in the base CSS file

```css
/* theme/static_src/src/input.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Custom component classes */
@layer components {
  .btn-primary {
    @apply py-2 px-4 bg-brand-primary text-white rounded-md hover:bg-opacity-90 focus:outline-none focus:ring-2 focus:ring-brand-primary focus:ring-opacity-50;
  }
}
```

## Accessibility Considerations

When using Tailwind CSS, maintain proper HTML semantics and ARIA attributes:

```html
<nav role="navigation" aria-label="Main navigation" class="bg-gray-800 text-white p-4">
  <ul class="flex space-x-4">
    <li><a href="/" class="hover:text-brand-primary">Home</a></li>
    <li><a href="/about" class="hover:text-brand-primary">About</a></li>
  </ul>
</nav>
```

## Best Practices with Our HTML-First Approach

1. **Start with semantic HTML first**:
   ```html
   <article>
     <header>
       <h1>Article Title</h1>
     </header>
     <section>
       <h2>Section Title</h2>
       <p>Content...</p>
     </section>
   </article>
   ```

2. **Add basic styling with PicoCSS**

3. **Use Django-HTMX for dynamic behavior**

4. **Only then, enhance with Tailwind utilities when necessary**:
   ```html
   <article class="max-w-prose mx-auto">
     <header class="border-b border-gray-200 mb-4 pb-2">
       <h1 class="text-3xl font-bold">Article Title</h1>
     </header>
     <section>
       <h2 class="text-xl font-semibold mb-2">Section Title</h2>
       <p class="leading-relaxed">Content...</p>
     </section>
   </article>
   ```

## Integration with Django-HTMX

Tailwind works well with HTMX for enhanced interactivity:

```html
<button 
  class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
  hx-get="/api/data"
  hx-target="#result"
  hx-swap="innerHTML"
>
  Load Data
</button>
<div id="result" class="mt-4 p-4 border rounded"></div>
```

## Resources

- [Django Tailwind Documentation](https://django-tailwind.readthedocs.io/en/latest/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Tailwind CSS GitHub Repository](https://github.com/tailwindlabs/tailwindcss)
- [Django Tailwind PyPI Package](https://pypi.org/project/django-tailwind/)
- [Django Tailwind GitHub Repository](https://github.com/timonweb/django-tailwind)
- [Tailwind CSS CLI Documentation](https://tailwindcss.com/docs/installation/tailwind-cli)

## Conclusion

While Django Tailwind offers powerful utility-based styling capabilities, remember our project's progressive enhancement principles:

1. Start with semantic HTML
2. Use PicoCSS for basic styling
3. Add Django-Hyperscript/HTMX for interactivity
4. Use Tailwind utilities only when necessary to achieve specific design requirements

This approach ensures our application remains accessible, semantic, and progressively enhanced while still benefiting from Tailwind's utility classes where needed.
