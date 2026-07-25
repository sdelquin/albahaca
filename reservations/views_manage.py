from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def index(request):
    context = {'section': 'Reservas'}
    return render(request, 'reservations/manage/index.html', context)
