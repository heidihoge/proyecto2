from django import template

register = template.Library()

@register.filter(name='intdot')
def intdot(field):
    try:
        return '{:,}'.format(field).replace(',', '.')

    except:
        return 0.0