from django.shortcuts import render

from .models import Image


def index(request):
    images = Image.objects.all()
    context = {'section': 'Galería', 'images': images}
    return render(request, 'gallery/index.html', context)
