from django.shortcuts import render

from .models import Info


def index(request):
    context = {'title': 'Contacto', 'info': Info.get()}
    return render(request, 'contact/index.html', context)
