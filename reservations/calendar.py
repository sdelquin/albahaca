import calendar
import datetime
import locale

from django.conf import settings
from django.db import models

from contact.models import Vacation

from .models import Reservation, Service, TableType


class Day:
    def __init__(self, date: datetime.date, *, management_mode: bool = False):
        self.date = date
        self.management_mode = management_mode
        self.build_services()
        self.check_for_reservation()

    def build_services(self) -> None:
        self.services = []
        now = datetime.datetime.now()
        for service in Service.get_services_for_date(self.date):
            service_data = {'service': service, 'enabled': True, 'details': '', 'table_types': []}
            if self.date == now.date() and now.time() > service.close_reservations_at:
                service_data['enabled'] = False
                service_data['details'] = 'No reservable: Muy próximo a horario'
            total_tables, reserved_tables = 0, 0
            for table_type in TableType.objects.all():
                table_type_data = {'table_type': table_type}
                table_type_data['total_tables'] = table_type.quantity
                table_type_data['reserved_tables'] = (
                    Reservation.objects.filter(
                        date=self.date,
                        time_slot__service=service,
                        table_types=table_type,
                    ).aggregate(
                        total_reserved=models.Sum('reservation_table_type_details__quantity')
                    )['total_reserved']
                    or 0
                )
                table_type_data['free_tables'] = (
                    table_type_data['total_tables'] - table_type_data['reserved_tables']
                )
                total_tables += table_type_data['total_tables']
                reserved_tables += table_type_data['reserved_tables']
                service_data['table_types'].append(table_type_data)
            service_data['reserved_percentage'] = reserved_tables / total_tables * 100
            if service_data['reserved_percentage'] == 100:
                service_data['enabled'] = False
                service_data['details'] = 'No reservable: Turno completo'
            self.services.append(service_data)

    def check_for_reservation(self) -> None:
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
        elif all(not s['enabled'] for s in self.services):
            self.enabled = False
            self.details = 'No reservable: Turnos completos'

    @property
    def day(self) -> int:
        return self.date.day

    @property
    def month(self) -> int:
        return self.date.month

    @property
    def year(self) -> int:
        return self.date.year

    @property
    def is_today(self) -> bool:
        return self.date == datetime.date.today()

    @property
    def isoformat(self) -> str:
        return self.date.isoformat()

    @property
    def name(self) -> str:
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        return self.date.strftime('%A %-d de %B de %Y').capitalize()

    def __repr__(self):
        return f'CalendarDay <{self.isoformat}>'


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
        self.only_days_belonging_to_month = only_days_belonging_to_month
        self.management_mode = management_mode
        self.build_dates()

    def build_dates(self) -> None:
        cal = calendar.Calendar()
        self.weeks = []
        for week in cal.monthdatescalendar(self.ref_year, self.ref_month):
            week_days = []
            for date in week:
                day = Day(date, management_mode=self.management_mode)
                day.belongs_to_month = not self.only_days_belonging_to_month or (
                    date.month == self.ref_month
                )
                week_days.append(day)
            self.weeks.append(week_days)

    def get_next_month(self) -> tuple:
        year = self.ref_year + (self.ref_month == 12)
        month = self.ref_month + 1
        return year, month

    @property
    def next_month(self) -> str:
        year, month = self.get_next_month()
        return f'{year:04d}{month:02d}'

    def get_previous_month(self) -> tuple:
        year = self.ref_year - (self.ref_month == 1)
        month = self.ref_month - 1
        return year, month

    @property
    def previous_month(self) -> str:
        year, month = self.get_previous_month()
        return f'{year:04d}{month:02d}'

    @property
    def name(self) -> str:
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        return calendar.month_name[self.ref_month].capitalize()

    def __str__(self) -> str:
        return f'{self.name} {self.ref_year}'
