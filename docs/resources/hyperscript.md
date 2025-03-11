# _hyperscript in Django

## Introduction

_hyperscript is a small scripting language designed for directly expressing user interface behavior in web applications. It follows the HTML-first development principles by adding behaviors directly within HTML elements, keeping the focus on semantic structure.

### Why Use _hyperscript in Django?

- **Progressive Enhancement**: Works alongside HTML as a natural extension
- **Declarative Syntax**: Expresses UI behavior in a readable format
- **Reduced JavaScript**: Minimizes the need for custom JavaScript
- **Integration**: Works seamlessly with Django templates and Django-HTMX

## Installation

Add django-hyperscript to your Django project:

```bash
pip install django-hyperscript
```

Then add it to your `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    # ...
    'django_hyperscript',
    # ...
]
```

Include the _hyperscript library in your base template:

```html
{% load hyperscript %}

<!DOCTYPE html>
<html>
<head>
    <!-- ... other head elements ... -->
    {% hyperscript_script %}
</head>
<body>
    <!-- Your content here -->
</body>
</html>
```

## Basic Syntax and Concepts

_hyperscript uses a simple, readable syntax:

### Event Handling

```html
<button _="on click toggle .active on me">Toggle Active</button>
```

### Variables and Control Flow

```html
<div _="on click
         set $count to parseInt(my.innerHTML)
         increment $count
         set my.innerHTML to $count">0</div>
```

### Working with Elements

```html
<button _="on click add .highlight to #target">Highlight</button>
<div id="target">This will be highlighted</div>
```

## Common Django Template Patterns

### Form Interaction

```html
<form _="on submit prevent default
            call fetch('/api/submit', {method: 'POST', body: new FormData(me)})
            then put 'Submitted!' into #status">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Submit</button>
    <p id="status"></p>
</form>
```

### Django Messages with _hyperscript

```html
<!-- In your base template -->
<div id="message-container">
    {% if messages %}
        {% for message in messages %}
            <div class="message {{ message.tags }}" _="on load wait 5s then add .fade-out
                                                     wait 0.5s then remove me">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
</div>
```

### Toggling Content

```html
<button _="on click toggle .hidden on #content">Show/Hide Content</button>
<div id="content" class="hidden">
    {% include 'partials/content.html' %}
</div>
```

## Integration with Django HTMX

_hyperscript works seamlessly with Django-HTMX for powerful UI interactions:

### Enhanced HTMX Requests

```html
<button hx-get="{% url 'load_data' %}"
        hx-target="#content"
        _="on htmx:afterOnLoad put 'Data loaded!' into #status">
    Load Data
</button>
<div id="content"></div>
<p id="status"></p>
```

### Managing Loading States

```html
<button hx-post="{% url 'process_form' %}"
        hx-target="#result"
        _="on htmx:beforeSend add .loading to me
           on htmx:afterOnLoad remove .loading from me">
    Submit
    <span class="spinner hidden" _="on htmx:beforeSend remove .hidden from me
                                   on htmx:afterOnLoad add .hidden to me"></span>
</button>
<div id="result"></div>
```

## Advanced Patterns

### Custom Events

```html
<div _="on customEvent(detail) log detail">
    <button _="on click send customEvent(detail:{message: 'Hello World'}) to the closest div">
        Trigger Event
    </button>
</div>
```

### Animations

```html
<button _="on click transition opacity to 0 on #target then remove #target">
    Fade Out & Remove
</button>
<div id="target">This content will fade out</div>
```

### Local Storage Interaction

```html
<div _="init
         if localStorage.getItem('darkMode') == 'true'
           add .dark-mode to body
         end">
    <button _="on click
               toggle .dark-mode on body
               set $isDark to body.classList.contains('dark-mode')
               set localStorage.darkMode to $isDark">
        Toggle Dark Mode
    </button>
</div>
```

### Django Form Validation with _hyperscript

```html
<form method="post" _="on submit prevent default
                        call fetch(my.action, {method: 'POST', body: new FormData(me)})
                            .then(response => response.json())
                        then if it.success
                            go to it.redirect_url
                        else
                            for error in it.errors
                                put error into the <p.error/> in #error-container
                            end">
    {% csrf_token %}
    {{ form.as_p }}
    <div id="error-container">
        <p class="error"></p>
    </div>
    <button type="submit">Submit</button>
</form>
```

## Best Practices

1. **Keep it Simple**: Use _hyperscript for behaviors that are logically tied to HTML elements.

2. **Progressive Enhancement**: Ensure basic functionality works without _hyperscript.

3. **Accessibility**: Maintain proper ARIA roles and keyboard navigation support.

   ```html
   <button _="on click or keyup[key=='Enter'] toggle .expanded on #details"
           aria-expanded="false"
           aria-controls="details">
       Toggle Details
   </button>
   <div id="details" hidden _="on click from previous add .expanded to me
                              on added.expanded to me set @hidden to false
                              on removed.expanded from me set @hidden to true">
       <!-- Details content -->
   </div>
   ```

4. **Avoid DOM Manipulation Logic**: For complex DOM changes, use Django views or components.

5. **Debug Mode**: Enable _hyperscript debugging for development:

   ```html
   <script>
       htmx.logAll();
       _hyperscript.config.debug = true;
   </script>
   ```

## Troubleshooting

### Common Issues

1. **Syntax Errors**:
   - Check browser console for _hyperscript syntax errors
   - Verify quotes and command structure

2. **Element Selection Issues**:
   - Use `closest`, `find`, `next` for relative selection
   - Ensure IDs and classes match your targets

3. **Timing Problems**:
   - Use the `wait` command for timing-dependent operations
   - Check event order with `log` statements

### Debug Commands

```html
<button _="on click log 'Button clicked' log event log me">Debug Button</button>
```

## Examples Gallery

### Collapsible Sections

```html
<div class="accordion">
    <h3 _="on click toggle .open on next <div/>
           toggle attr aria-expanded between 'true' 'false' on me"
        aria-expanded="false">
        Section Title
    </h3>
    <div class="accordion-content" hidden
         _="on added.open to me remove @hidden
            on removed.open from me add @hidden">
        Accordion content here
    </div>
</div>
```

### Dynamic Form Fields

```html
<div id="form-fields">
    <div class="field-row">
        <input type="text" name="item[]">
        <button type="button" _="on click remove closest .field-row">Remove</button>
    </div>
</div>
<button type="button" 
        _="on click put '<div class=\"field-row\"><input type=\"text\" name=\"item[]\"><button type=\"button\" _=\"on click remove closest .field-row\">Remove</button></div>' at end of #form-fields">
    Add Field
</button>
```

### Conditional Form Fields

```html
<select name="contact_preference" _="on change 
                                      if my.value == 'phone' 
                                        remove .hidden from #phone-field
                                        add .hidden to #email-field
                                      else
                                        add .hidden to #phone-field
                                        remove .hidden from #email-field">
    <option value="email">Email</option>
    <option value="phone">Phone</option>
</select>

<div id="email-field">
    <label>Email: <input type="email" name="email"></label>
</div>

<div id="phone-field" class="hidden">
    <label>Phone: <input type="tel" name="phone"></label>
</div>
```

## Resources and References

- [Official _hyperscript Documentation](https://hyperscript.org/docs/)
- [_hyperscript Reference](https://hyperscript.org/reference/)
- [Django-hyperscript GitHub Repository](https://github.com/LucLor06/django-hyperscript)
- [_hyperscript Cookbook](https://hyperscript.org/cookbook/)
- [Django HTMX Starter Kit](https://github.com/hypebeast/django-htmx-starterkit)

## Real-world Examples

For additional examples of _hyperscript in Django projects, check:
- [Django Message Popups with _hyperscript](https://aviitala.com/posts/django-message-popups-with-hyperscript-and-css/)
- [_hyperscript Main Repository](https://github.com/bigskysoftware/_hyperscript)

## Conclusion

_hyperscript provides a lightweight, powerful way to add interactivity to your Django applications while maintaining HTML-first principles. By writing behaviors directly in your templates, you create more maintainable code that aligns with progressive enhancement strategies.
