from django import template

register = template.Library()

@register.filter(name='dias')
def dias(field):
    values = (('Lunes', field.lunes), ('Martes', field.martes), ('Miercoles', field.miercoles),
              ('Jueves', field.jueves), ('Viernes', field.viernes), ('Sabado', field.sabado), ('Domingo', field.domingo))

    return ", ".join(list(map(lambda x: x[0], filter(lambda x: x[1], values))))