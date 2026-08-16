import calendar
import datetime
import locale
from collections import defaultdict

from django.conf import settings
from django.db import models

from contact.models import Vacation

from .models import Reservation, Service, TableType, TimeSlot


class Day:
    def __init__(self, date: datetime.date, *, management_mode: bool = False):
        self.date = date
        self.management_mode = management_mode

    def check_for_reservation(self) -> None:
        self.services = Service.get_services_for_date(self.date)
        self.enabled, self.details = True, ''
        if self.date < (today := datetime.date.today()):
            self.enabled = False
            self.details = 'No reservable: Pasado'
        elif Vacation.is_vacation(self.date):
            self.enabled = False
            self.details = 'No reservable: Vacaciones'
        elif not self.management_mode and self.date > (
            today + datetime.timedelta(days=settings.OPEN_RESERVATIONS_DAYS)
        ):
            self.enabled = False
            self.details = 'No reservable: Muy lejano a horario'
        elif not self.services:
            self.enabled = False
            self.details = 'No reservable: Cerrado'

    def fetch_service_details(self) -> None:
        self.services = []
        now = datetime.datetime.now()
        for service in Service.get_services_for_date(self.date):
            service.enabled = True
            service.details = ''
            service.table_types = []
            if self.date == now.date() and now.time() > service.time_slots.last().time:
                service.enabled = False
                service.details = 'No reservable: Pasado'
            elif (
                not self.management_mode
                and self.date == now.date()
                and now.time() > service.close_reservations_at
            ):
                service.enabled = False
                service.details = 'No reservable: Muy próximo a horario'
            total_tables, reserved_tables = 0, 0
            for table_type in TableType.objects.all():
                table_type.total_tables = table_type.quantity
                table_type.reserved_tables = (
                    Reservation.objects.filter(
                        date=self.date,
                        time_slot__service=service,
                        table_types=table_type,
                    ).aggregate(
                        total_reserved=models.Sum('reservation_table_type_details__quantity')
                    )['total_reserved']
                    or 0
                )
                table_type.free_tables = table_type.total_tables - table_type.reserved_tables
                total_tables += table_type.total_tables
                reserved_tables += table_type.reserved_tables
                service.table_types.append(table_type)
            service.reserved_percentage = reserved_tables / total_tables * 100
            if service.reserved_percentage == 100:
                service.enabled = False
                service.details = 'No reservable: Turno completo'
            self.services.append(service)

    @property
    def is_today(self) -> bool:
        return self.date == datetime.date.today()

    def __repr__(self):
        return f'CalendarDay <{self.date.isoformat}>'

    def get_service_from_time_slot(self, time_slot: TimeSlot) -> Service | None:
        for service in self.services:
            if service == time_slot.service:
                return service
        return None

    def fetch_table_types_for_reservation(
        self, time_slot: TimeSlot, party_size: int
    ) -> dict | None:
        service = self.get_service_from_time_slot(time_slot)
        left_party_size = party_size
        assigned_table_types = defaultdict(int)
        while left_party_size > 0:
            # Encontrar el tipo de mesa libre más cercana a las personas que faltan por colocar
            min_distance = 1024
            assigned_table_type = None
            for table_type in service.table_types:
                if table_type.free_tables == 0:
                    continue
                if (distance := abs(table_type.seats - left_party_size)) <= min_distance:
                    min_distance = distance
                    assigned_table_type = table_type
            if not assigned_table_type:
                return None
            left_party_size = max(left_party_size - assigned_table_type.seats, 0)
            assigned_table_type.free_tables -= 1
            assigned_table_type.reserved_tables += 1
            assigned_table_types[assigned_table_type] += 1
        return assigned_table_types


class Month:
    def __init__(
        self,
        ref_year: int | None = None,
        ref_month: int | None = None,
        *,
        management_mode: bool = False,
        only_days_belonging_to_month: bool = True,
    ):
        today = datetime.date.today()
        self.ref_year = ref_year or today.year
        self.ref_month = ref_month or today.month
        self.is_current_month = self.current_month == (self.ref_year, self.ref_month)
        self.only_days_belonging_to_month = only_days_belonging_to_month
        self.management_mode = management_mode
        self.add_days()

    def add_days(self) -> None:
        cal = calendar.Calendar()
        self.weeks = []
        for week in cal.monthdatescalendar(self.ref_year, self.ref_month):
            week_days = []
            for date in week:
                day = Day(date, management_mode=self.management_mode)
                day.check_for_reservation()
                day.belongs_to_month = not self.only_days_belonging_to_month or (
                    date.month == self.ref_month
                )
                week_days.append(day)
            self.weeks.append(week_days)

    @property
    def next_month(self) -> tuple:
        year = self.ref_year + (self.ref_month == 12)
        month = self.ref_month + 1 if self.ref_month < 12 else 1
        return year, month

    @property
    def current_month(self) -> tuple:
        today = datetime.date.today()
        return today.year, today.month

    @property
    def previous_month(self) -> tuple:
        year = self.ref_year - (self.ref_month == 1)
        month = self.ref_month - 1 if self.ref_month > 1 else 12
        return year, month

    @property
    def name(self) -> str:
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        return calendar.month_name[self.ref_month].capitalize()

    def __str__(self) -> str:
        return f'{self.name} {self.ref_year}'
