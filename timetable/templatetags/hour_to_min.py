from django import template

register = template.Library()

@register.filter
def hour_to_min(value):
    value = str(value)
    try:
        hour, min, sec = value.split(':')
        return int(hour)*60 + int(min)
    except:
        hour, min = value.split(':')
        return int(hour) * 60 + int(min)
    return value.replace(-1)
