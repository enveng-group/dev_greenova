# Pico CSS Learning Resource

## Introduction

[Pico CSS](https://picocss.com/) is a minimal CSS framework designed to build
elegant, responsive websites with semantic HTML. It prioritizes semantic HTML,
focuses on progressive enhancement, and provides beautiful baseline styling
with minimal effort.

## Key Features

- **Minimal (~14KB minified and gzipped)**
- **Semantic** - Uses native HTML elements and attributes instead of custom classes
- **Responsive** - Mobile-first approach with responsive typography and spacing
- **Classless** - Can be used without any custom classes
- **Customizable** - Easy to customize with CSS variables
- **Dark Mode** - Built-in light/dark theme support

## Installation Options

### CDN Integration

```html
<!-- Minimal CSS reset (Eric Meyer) -->
<link
  rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css"
/>
```

### NPM Installation

```bash
npm install @picocss/pico
```

Then import it in your project:

```javascript
import '@picocss/pico';
```

### Classless Mode

Pico's classless mode allows for styling with semantic HTML without requiring
custom CSS classes. This aligns with our project's HTML-first development
approach.

Example:
Pico's classless mode allows for styling with semantic HTML without requiring custom CSS classes. This aligns with our project's HTML-first development approach.

Example:

```html
<main class="container">
  <h1>Hello, Pico CSS!</h1>
  <p>This is a paragraph with automatic styling from Pico.</p>

  <!-- Forms -->
  <form>
    <label for="email">Email</label>
    <input type="email" id="email" name="email" placeholder="Email" required />

    <label for="message">Message</label>
    <textarea
      id="message"
      name="message"
      placeholder="Message"
      required
    ></textarea>

    <button type="submit">Submit</button>
  </form>
</main>
```

### With CSS Classes

For more complex layouts, Pico provides utility classes:

```html
<div class="container">
  <div class="grid">
    <div>Grid item 1</div>
    <div>Grid item 2</div>
  </div>
</div>
```

## Core Components

### Grid System

Pico uses a responsive grid layout:

```html
<div class="grid">
  <div>Column 1</div>
  <div>Column 2</div>
  <div>Column 3</div>
</div>
```

For different grid layouts:

```html
<!-- 2-column grid -->
<div class="grid">
  <div>Column 1</div>
  <div>Column 2</div>
</div>

<!-- 3-column grid -->
<div class="grid">
  <div>Column 1</div>
  <div>Column 2</div>
  <div>Column 3</div>
</div>
```

### Forms

Forms automatically get styled:

```html
<form>
  <fieldset>
    <label for="firstname">First name</label>
    <input
      type="text"
      id="firstname"
      name="firstname"
      placeholder="First name"
      required
    />

    <label for="lastname">Last name</label>
    <input
      type="text"
      id="lastname"
      name="lastname"
      placeholder="Last name"
      required
    />

    <label for="email">Email</label>
    <input type="email" id="email" name="email" placeholder="Email" required />
  </fieldset>

  <fieldset>
    <label for="terms">
      <input type="checkbox" id="terms" name="terms" />
      I agree to the Terms and Conditions
    </label>
  </fieldset>

  <button type="submit">Submit</button>
</form>
```

### Cards

Create cards with simple HTML:

```html
<article>
  <header>Card Header</header>
  <p>Card content goes here.</p>
  <footer>Card Footer</footer>
</article>
```

## Customization

Pico uses CSS variables for easy customization:

```css
:root {
  /* Primary colors */
  --primary: #1095c1;
  --primary-hover: #08769b;

  /* Typography */
  --font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
  --font-size: 16px;
  --line-height: 1.5;

  /* Spacing */
  --spacing: 1rem;
  --border-radius: 0.25rem;
}
```

<!-- Light theme by default -->
<html lang="en" data-theme="light">
<head>
  <title>Page Title</title>
  <meta name="description" content="Description of the page">
  <meta name="keywords" content="pico, css, theme, light">
  <!-- Content -->
</head>
<body>
  <!-- Content -->
</body>
</html>

<!-- Dark theme by default -->
<html lang="en" data-theme="dark">
<head>
  <title>Page Title</title>
  <meta name="description" content="Description of the page">
  <meta name="keywords" content="pico, css, theme, dark">
  <!-- Content -->
</head>
<body>
  <!-- Content -->
</body>
</html>

<!-- Auto theme by default -->
<html lang="en" data-theme="auto">
<head>
  <title>Page Title</title>
1. Add the CDN link in your base template:
  <meta name="keywords" content="pico, css, theme, auto">
  <!-- Content -->
{% block styles %}
<link
  rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css"
/>
{% endblock styles %}
    <!-- Auto theme by default (based on user's system preference) -->
    <html data-theme="auto"></html>
  </html>
</html>
```

Toggle between themes with JavaScript:

- Use appropriate HTML5 elements (header, main, section, etc.)
  // Function to toggle themes
  function toggleTheme() {
  const html = document.documentElement;
  const currentTheme = html.getAttribute('data-theme');

if (currentTheme === 'dark') {
html.setAttribute('data-theme', 'light');
} else {
html.setAttribute('data-theme', 'dark');
}
}

````

## Integration with Django

To use Pico CSS with Django templates:

1. Add the CDN link in your base template:

```html
{% block styles %}
<link
  rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css"
/>
{% endblock %}
````

2. Or install via npm and include in your static files

## Best Practices for Greenova Project

1. **Follow semantic HTML structure**

   - Use appropriate HTML5 elements (`<header>`, `<main>`, `<section>`, etc.)
   - Maintain proper heading hierarchy (h1-h6)

2. **Progressive enhancement**

   - Start with well-structured HTML
   - Layer PicoCSS for styling
   - Add JavaScript interactivity only when necessary

3. **Accessibility**

   - Use proper ARIA attributes where needed
   - Ensure forms have proper labels
   - Maintain good color contrast

4. **Mobile-first approach**
   - Design for mobile first, then enhance for larger screens
   - Test on various screen sizes

## Useful Resources

- [Pico CSS Official Website](https://picocss.com/)
- [Documentation](https://picocss.com/docs)
- [Classless Documentation](https://picocss.com/docs/classless)
- [GitHub Repository](https://github.com/picocss/pico)
- [Examples](https://picocss.com/examples)

## Integration with Project's HTML-First Development

Pico CSS aligns perfectly with our project's HTML-first development approach:

1. It prioritizes semantic HTML
2. Follows progressive enhancement principles
3. Works well with Django templates
4. Supports accessibility best practices
5. Can be extended with Django-Tailwind for more complex utility needs
