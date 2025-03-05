# <_> Hyperscript ~ Documentation

# Change from Django Template Logic to Hyperscript

## Original Code (Django Template)

```html
{% if not request.user.is_authenticated %}
    <nav>
        <a href="{% url 'authentication:register' %}" role="button" class="primary">Get Started</a>
        <a href="#features" role="button" class="outline">Learn More</a>
    </nav>
{% endif %}
```

## Refactored Code (Hyperscript Template)
```html
<nav _="on load if user_authenticated then show else hide">
<a href="{% url 'authentication:register' %}"
    role="button"
    class="primary">Get Started</a>
<a href="#features" role="button" class="outline">Learn More</a>
</nav>
```
