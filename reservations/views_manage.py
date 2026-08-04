import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .calendar import Month
from .models import Weekday


@login_required
def index(request):
    context = {
        'section': 'Reservas',
        'month': Month(management_mode=True),
        'weekdays': Weekday.objects.all(),
    }
    return render(request, 'reservations/manage/index.html', context)


@login_required
def month(request, year: int = None, month: int = None):
    today = datetime.date.today()
    year = year or today.year
    month = month or today.month
    context = {
        'month': Month(year, month, management_mode=True),
        'weekdays': Weekday.objects.all(),
        'current_month': (today.year, today.month),
    }
    return render(request, 'reservations/manage/partials/reservation_month.html', context)
