def site_context(request):
    """
    Adds the current site to the context.
    """
    return {'site': getattr(request, 'site', 'public')}
