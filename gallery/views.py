from django.conf import settings
from django.shortcuts import render

from .models import Image


def index(request):
    images = Image.objects.all()
    context = {
        'section': 'Galería',
        'images': images,
        'thumbnail_size': settings.THUMBNAILS_SIZE,
    }
    return render(request, 'gallery/index.html', context)
