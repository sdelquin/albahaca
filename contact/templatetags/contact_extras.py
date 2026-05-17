from django import template

from contact.models import Info

register = template.Library()


@register.inclusion_tag('contact/includes/social.html')
def social_links():
    info = Info.get()
    data = []
    for line in info.social.splitlines():
        service, icon, url = line.split('|')
        data.append({'service': service.strip(), 'icon': icon.strip(), 'url': url.strip()})
    return {'data': data}
