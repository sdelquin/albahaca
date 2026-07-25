from django.shortcuts import render


def index(request):
    return render(request, 'homepage/public/index.html')
