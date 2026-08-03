from django import template

register = template.Library()


@register.filter
def reservation_level(service: dict):
    rp = service['reserved_percentage']
    if rp < 40:
        return 'text-green-500'
    elif rp < 80:
        return 'text-orange-500'
    else:
        return 'text-red-500'
