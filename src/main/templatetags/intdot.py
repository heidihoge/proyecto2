from django import template

register = template.Library()

@register.filter(name='intdot')
def intdot(field):
    return '{:,}'.format(field).replace(',','.')