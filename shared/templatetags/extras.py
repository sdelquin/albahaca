import os
from datetime import date, datetime

from django import template
from django.conf import settings
from django.contrib.staticfiles.finders import find
from django.templatetags.static import static
from django.urls import NoReverseMatch, reverse
from django.utils.formats import date_format
from django.utils.translation import override

register = template.Library()


@register.simple_tag
def hashed_static(static_path: str) -> str:
    """
    Hashed static.
    Inspiration: https://www.reddit.com/r/django/comments/ychowr/comment/itqnrvv/
    """
    url_path = static(static_path)
    if fs_path := find(static_path):
        if settings.DEBUG:
            return url_path
        last_modification = os.path.getmtime(fs_path)
        return f'{url_path}?v={last_modification}'
    raise FileNotFoundError(f'Static file not found: {static_path}')


@register.inclusion_tag('includes/navitem.html', takes_context=True)
def navitem(context, url_name, title):
    request = context['request']
    try:
        url = reverse(url_name)
    except NoReverseMatch:
        url = 'javascript:alert("Próximamente")'
    active = request.path.startswith(url)
    return {'url': url, 'active': active, 'title': title}


@register.filter
def datetime_es(value, fmt=r'l j \d\e F \d\e Y'):
    if not isinstance(value, (date, datetime)):
        return value

    with override('es'):
        text = date_format(value, fmt, use_l10n=True)
        return text.capitalize()
