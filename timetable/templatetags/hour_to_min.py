from django import template

register = template.Library()


@register.filter
def hour_to_min(value):
    value = str(value)

    try:
        day = 0
        hour = 0
        min = 0
        sec = 0
        # in shape of 1 day, 0:00:00
        if 'day' in value:
            day = value.split(',')[0].split(' ')[0]
            hour, min, sec = value.split(', ')[-1].split(':')
        # in shape of 0:00:00
        else:
            hour, min, sec = value.split(':')
        return int(day) * 24 * 60 + int(hour) * 60 + int(min)
    except:
        day = 0
        hour = 0
        min = 0
        sec = 0
        # in shape of 1 day, 0:00
        if 'day' in value:
            day = value.split(',')[0].split(' ')[0]
            hour, min = value.split(', ')[-1].split(':')
        # in shape of 0:00
        else:
            hour, min = value.split(':')
        return int(day) * 24 * 60 + int(hour) * 60 + int(min)

    return value.replace(-1)
