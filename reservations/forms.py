from django import forms

from .models import Service


class DateReservationForm(forms.Form):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Fecha de la reserva',
        input_formats=['%Y-%m-%d'],
    )

    def clean_date(self):
        if (date := self.cleaned_data['date']) < forms.fields.datetime.date.today():
            raise forms.ValidationError('La fecha de la reserva no puede ser en el pasado.')
        if date.weekday() not in Service.get_available_weekdays():
            raise forms.ValidationError('No hay turnos disponibles para la fecha seleccionada.')
        return date
