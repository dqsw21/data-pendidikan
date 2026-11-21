from django import template

register = template.Library()

@register.filter
def format_indonesia(value):
    try:
        number = int(value)
        return f"{number:,}".replace(",", ".")
    except (ValueError, TypeError):
        return value
