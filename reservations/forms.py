import re

from django import forms
from django.conf import settings

from .models import TableType


class CreateReservationForm(forms.Form):
    time_slot = forms.ChoiceField(label='Hora', choices=[])
    zone = forms.ChoiceField(label='Zona', choices=TableType.Zone.choices)
    name = forms.CharField(label='Nombre', max_length=256)
    party_size = forms.IntegerField(label='Número de comensales', min_value=1)
    phone = forms.CharField(label='Teléfono', max_length=20)
    remarks = forms.CharField(
        label='Observaciones',
        widget=forms.Textarea(attrs={'rows': 4}),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        time_slot_choices = kwargs.pop('time_slot_choices', [])
        self.management_mode = kwargs.pop('management_mode', False)
        super().__init__(*args, **kwargs)
        self.fields['time_slot'].choices = time_slot_choices

    def clean_party_size(self):
        party_size = self.cleaned_data.get('party_size')
        if not self.management_mode and party_size > settings.MAX_PARTY_SIZE:
            raise forms.ValidationError(
                f'El número máximo permitido de comensales es {settings.MAX_PARTY_SIZE}. Para reservas más grandes, por favor contacte con el restaurante directamente.'
            )
        return party_size

    def clean_phone(self):
        if (phone := self.cleaned_data.get('phone')) and not re.fullmatch(
            settings.PHONE_REGEX, phone
        ):
            raise forms.ValidationError(
                'El formato del teléfono no es válido. Ejemplos válidos: 675432189 o +34 675432189'
            )
        return phone
