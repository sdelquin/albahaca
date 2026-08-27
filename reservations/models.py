import datetime

from django.db import models


class Weekday(models.Model):
    name = models.CharField(max_length=20, verbose_name='Nombre')
    code = models.PositiveSmallIntegerField(unique=True, verbose_name='Código')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Día de la semana'
        verbose_name_plural = 'Días de la semana'
        ordering = ['code']


class TableType(models.Model):
    class Zone(models.TextChoices):
        INDOOR = 'I', 'Interior'
        TERRACE = 'T', 'Terraza'

    seats = models.PositiveSmallIntegerField(verbose_name='Número de asientos')
    quantity = models.PositiveSmallIntegerField(verbose_name='Cantidad de mesas disponibles')
    zone = models.CharField(
        max_length=2, choices=Zone.choices, default=Zone.INDOOR, verbose_name='Zona'
    )

    @property
    def code(self) -> str:
        return f'{self.zone}{self.seats}'

    def __str__(self):
        return f'Mesa {self.seats}p ({self.get_zone_display()})'

    class Meta:
        verbose_name = 'Tipos de mesa'
        verbose_name_plural = 'Tipos de mesas'
        ordering = ['zone', 'seats']


class Service(models.Model):
    name = models.CharField(max_length=256, verbose_name='Nombre')
    code = models.CharField(max_length=1, unique=True, verbose_name='Código')
    close_reservations_at = models.TimeField(verbose_name='Hora límite para realizar reservas')
    available_at = models.ManyToManyField(
        Weekday, verbose_name='Turno disponible estos días', related_name='services'
    )

    def __str__(self):
        return self.name

    @classmethod
    def get_services_for_date(cls, date: datetime.date) -> models.QuerySet:
        weekday = date.weekday()  # 0=Monday, 6=Sunday
        return Service.objects.filter(available_at__code=weekday)

    @classmethod
    def get_available_weekdays(cls) -> set[int]:
        return set(cls.objects.order_by().values_list('available_at__code', flat=True).distinct())

    class Meta:
        verbose_name = 'Turno'
        verbose_name_plural = 'Turnos'
        ordering = ['close_reservations_at']


class TimeSlot(models.Model):
    time = models.TimeField(verbose_name='Hora')
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, verbose_name='Turno asociado', related_name='time_slots'
    )

    class Meta:
        verbose_name = 'Franja horaria'
        verbose_name_plural = 'Franjas horarias'
        ordering = ['time']
        unique_together = ('time', 'service')

    def __str__(self):
        return f'{self.time.strftime("%H:%M")}h'


class ReservationTableTypeDetail(models.Model):
    reservation = models.ForeignKey(
        'reservations.Reservation',
        related_name='reservation_table_type_details',
        on_delete=models.CASCADE,
    )
    table_type = models.ForeignKey(
        'reservations.TableType',
        related_name='reservation_tabletype_details',
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveSmallIntegerField(verbose_name='Cantidad', default=1)

    class Meta:
        verbose_name = 'Detalle de tipo de mesa de reserva'
        verbose_name_plural = 'Detalles de tipos de mesa de reserva'
        unique_together = ('reservation', 'table_type')

    def __str__(self):
        return f'{self.table_type} ({self.quantity} ud.)'


class Reservation(models.Model):
    name = models.CharField(max_length=256, verbose_name='Nombre')
    phone = models.CharField(max_length=20, verbose_name='Teléfono')
    date = models.DateField(verbose_name='Fecha')
    time_slot = models.ForeignKey(
        TimeSlot, on_delete=models.CASCADE, verbose_name='Hora', related_name='reservations'
    )
    party_size = models.PositiveSmallIntegerField(verbose_name='Número de comensales')
    table_types = models.ManyToManyField(
        TableType,
        verbose_name='Tipos de mesas',
        related_name='reservations',
        through='reservations.ReservationTableTypeDetail',
    )
    remarks = models.TextField(blank=True, verbose_name='Observaciones')
    managed_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Profesional que gestionó la reserva',
        related_name='reservations',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    arrived_at = models.DateTimeField(null=True, blank=True, verbose_name='Llegada')

    def __str__(self):
        return f'{self.name} - {self.date} {self.time_slot} - {self.party_size} comensales'

    def get_table_types_display(self) -> str:
        details = self.reservation_table_type_details.select_related('table_type').order_by(
            'table_type__seats'
        )
        buf = []
        for detail in details:
            item = detail.table_type.code
            if (q := detail.quantity) > 1:
                item += f'x{q}'
            buf.append(item)
        return ' + '.join(buf)

    def anonymize(self) -> None:
        self.name = '#' * len(str(self.name))  # type: ignore
        self.phone = '#' * len(str(self.phone))  # type: ignore
        self.save()

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
        ordering = ['-date', 'time_slot__time', 'created_at']
