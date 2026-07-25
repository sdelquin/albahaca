from django.conf import settings


class HostURLConfMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().split(':')[0].lower()

        if host.startswith(settings.MANAGE_PREFIX):
            request.urlconf = 'main.urls_manage'
            request.site = 'manage'
        else:
            request.urlconf = 'main.urls_public'
            request.site = 'public'

        if settings.SWAP_BASE_DOMAINS:
            request.urlconf = (
                'main.urls_manage' if request.urlconf == 'main.urls_public' else 'main.urls_public'
            )
            request.site = 'manage' if request.site == 'public' else 'public'

        return self.get_response(request)
