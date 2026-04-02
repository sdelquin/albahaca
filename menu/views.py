from django.shortcuts import render

from .models import Category


def index(request):
    categories = Category.objects.all()
    context = {'section': 'Carta', 'categories': categories}
    return render(request, 'menu/index.html', context)
