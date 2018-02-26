from django import template

register = template.Library()

@register.filter(name='field_type')
def field_type(field):
    return type(field.field).__name__