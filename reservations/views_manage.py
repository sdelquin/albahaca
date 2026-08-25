import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .calendar import Day, Month
from .forms import CreateReservationForm
from .models import Reservation, Service, TimeSlot, Weekday


@login_required
def index(request):  # noqa
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
def services(request, year: int, month: int, day: int):
    date = datetime.date(year, month, day)
    target_month = Month(year, month, management_mode=True)
    target_day = Day(date, management_mode=True)
    target_day.check_for_reservation()
    target_day.fetch_service_details()
    context = {
        'title': 'Reservas',
        'month': target_month,
        'day': target_day,
    }
    if request.htmx:
        return render(request, 'reservations/manage/partials/services.html', context)
    return render(request, 'reservations/manage/index.html', context)


@login_required
def service(request, year: int, month: int, day: int, service_code: str):
    date = datetime.date(year, month, day)
    target_month = Month(year, month, management_mode=True)
    target_day = Day(date, management_mode=True)
    target_day.check_for_reservation()
    target_day.fetch_service_details()
    service = Service.objects.get(code=service_code)
    context = {
        'title': 'Reservas',
        'month': target_month,
        'day': target_day,
        'selected_service': service,
    }
    if request.htmx:
        return render(request, 'reservations/manage/partials/services.html', context)
    return render(request, 'reservations/manage/index.html', context)


@login_required
def list_service_reservations(request, year: int, month: int, day: int, service_code: str):
    date = datetime.date(year, month, day)
    target_month = Month(year, month, management_mode=True)
    target_day = Day(date, management_mode=True)
    target_day.check_for_reservation()
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
        return render(
            request, 'reservations/manage/partials/service/list_reservations.html', context
        )
    return render(request, 'reservations/manage/index.html', context)


@login_required
def create_service_reservation(request, year: int, month: int, day: int, service_code: str):
    date = datetime.date(year, month, day)
    target_month = Month(year, month, management_mode=True)
    target_day = Day(date, management_mode=True)
    target_day.check_for_reservation()
    target_day.fetch_service_details()
    service = Service.objects.get(code=service_code)
    time_slots_choices = service.time_slots.all().values_list('id', 'time')
    if request.method == 'POST':
        form = CreateReservationForm(
            request.POST, time_slot_choices=time_slots_choices, management_mode=True
        )
        if form.is_valid():
            time_slot_id = form.cleaned_data['time_slot']
            time_slot = TimeSlot.objects.get(id=time_slot_id)
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            party_size = form.cleaned_data['party_size']
            remarks = form.cleaned_data['remarks']
            if table_types := target_day.fetch_table_types_for_reservation(time_slot, party_size):
                reservation = Reservation.objects.create(
                    date=date,
                    time_slot=time_slot,
                    name=name,
                    phone=phone,
                    party_size=party_size,
                    remarks=remarks,
                    managed_by=request.user if request.user.is_authenticated else None,
                )
                for table_type, quantity in table_types.items():
                    if quantity > 0:
                        reservation.table_types.add(
                            table_type, through_defaults={'quantity': quantity}
                        )
                context = {
                    'day': target_day,
                    'reservation': reservation,
                }
                return render(
                    request,
                    'reservations/manage/partials/service/reservation_created.html',
                    context,
                )
            else:
                form.add_error(
                    None,
                    'No hay suficientes mesas disponibles para el tamaño de la reserva. Por favor, seleccione otro turno o reduzca el número de comensales.',
                )
    else:
        form = CreateReservationForm(time_slot_choices=time_slots_choices, management_mode=True)
    context = {
        'title': 'Reservas',
        'month': target_month,
        'day': target_day,
        'selected_service': service,
        'form': form,
    }
    if request.htmx:
        return render(
            request, 'reservations/manage/partials/service/create_reservation.html', context
        )
    return render(request, 'reservations/manage/index.html', context)
