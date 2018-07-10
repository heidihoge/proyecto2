from django import template

register = template.Library()

@register.filter(name='intdot')
def intdot(field):

    if type(field) == str:
        try:
            return '{:,}'.format(int(field)).replace(',', '.')
        except:
            return field
    try:

        return '{:,}'.format(field).replace(',', '.')

    except Exception as e:
        print(e)
        return 0.0