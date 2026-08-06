def site_context(request):
    """
    Adds the current site to the context.
    """
    return {'manage': getattr(request, 'site', 'public') == 'manage'}
