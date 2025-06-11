from django import template

register = template.Library()


@register.filter
def sum_field(items, field_name):
    """Sum a numeric field across a list of dicts or objects."""
    total = 0
    for item in items:
        value = 0
        if isinstance(item, dict):
            value = item.get(field_name, 0)
        else:
            value = getattr(item, field_name, 0)
        try:
            total += int(value)
        except (TypeError, ValueError):
            continue
    return total
