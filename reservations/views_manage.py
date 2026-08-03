from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .calendar import Month
from .forms import DateReservationForm
from .models import Weekday


@login_required
def index(request):
    context = {'section': 'Reservas', 'month': Month(), 'weekdays': Weekday.objects.all()}
    return render(request, 'reservations/manage/index.html', context)


@login_required
def create_phase_date(request):
    if request.method == 'POST':
        if (form := DateReservationForm(request.POST)).is_valid():
            # Aquí puedes procesar la reserva, por ejemplo, guardarla en la base de datos
            # Por ahora, simplemente redirigimos a la página de índice de reservas
            return render(request, 'reservations/manage/index.html', {'section': 'Reservas'})
    else:
        form = DateReservationForm()

    context = {
        'form': form,
        'section': 'Crear Reserva',
    }
    return render(request, 'reservations/manage/create/date.html', context)
