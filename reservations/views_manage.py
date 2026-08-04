from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .calendar import Month
from .models import Weekday


@login_required
def index(request):
    if month_qs := request.GET.get('mes'):
        year = int(month_qs[:4])
        month = int(month_qs[4:])
    else:
        year, month = None, None
    context = {
        'section': 'Reservas',
        'month': Month(year, month, management_mode=True),
        'weekdays': Weekday.objects.all(),
    }
    return render(request, 'reservations/manage/index.html', context)
