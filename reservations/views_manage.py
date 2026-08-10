import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .calendar import Day, Month
from .models import Reservation, Service, Weekday


@login_required
def index(request):
    today = datetime.date.today()
    return redirect('reservations:month', year=today.year, month=today.month)


@login_required
def month(request, year: int, month: int):
    target_month = Month(year, month, management_mode=True)
    context = {
        'title': 'Reservas',
        'month': target_month,
        'weekdays': Weekday.objects.all(),
    }
    if request.htmx:
        return render(request, 'reservations/manage/partials/month.html', context)
    return render(request, 'reservations/manage/index.html', context)


@login_required
def day(request, year: int, month: int, day: int):
    date = datetime.date(year, month, day)
    target_month = Month(year, month, management_mode=True)
    target_day = Day(date, management_mode=True)
    target_day.fetch_service_details()
    context = {
        'title': 'Reservas',
        'month': target_month,
        'day': target_day,
    }
    if request.htmx:
        return render(request, 'reservations/manage/partials/day.html', context)
    return render(request, 'reservations/manage/index.html', context)


@login_required
def service(request, year: int, month: int, day: int, service_code: str):
    date = datetime.date(year, month, day)
    target_month = Month(year, month, management_mode=True)
    target_day = Day(date, management_mode=True)
    target_day.fetch_service_details()
    service = Service.objects.get(code=service_code)
    reservations = Reservation.objects.filter(date=date, time_slot__service=service)
    context = {
        'title': 'Reservas',
        'month': target_month,
        'day': target_day,
        'selected_service': service,
        'reservations': reservations,
    }
    if request.htmx:
        return render(request, 'reservations/manage/partials/service.html', context)
    return render(request, 'reservations/manage/index.html', context)
