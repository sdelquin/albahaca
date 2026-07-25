from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from homepage.views_manage import index

urlpatterns = [
    path('__reload__/', include('django_browser_reload.urls')),
    path('', index, name='index'),
    path('', include('accounts.urls')),
    path('reservas/', include('reservations.urls_manage')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
