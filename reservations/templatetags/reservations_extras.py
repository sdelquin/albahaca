from django import template

register = template.Library()


@register.filter
def reservation_level(service: dict):
    rp = service['reserved_percentage']
    if rp < 20:
        return 'text-green-500'
    if rp < 60:
        return 'text-yellow-500'
    if rp < 100:
        return 'text-orange-500'
    return 'text-red-500'
