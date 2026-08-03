from django.contrib import admin

from .models import (
    Reservation,
    ReservationTableTypeDetail,
    Service,
    TableType,
    TimeSlot,
    Weekday,
)


class TimeSlotInline(admin.TabularInline):
    model = TimeSlot
    extra = 0


class ReservationTableTypeDetailInline(admin.TabularInline):
    model = ReservationTableTypeDetail
    extra = 0


@admin.register(Weekday)
class WeekdayAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')


@admin.register(TableType)
class TableTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'seats', 'quantity')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'close_reservations_at', 'get_available_days')
    filter_horizontal = ('available_at',)
    inlines = [TimeSlotInline]

    @admin.display(description='Días disponibles')
    def get_available_days(self, obj):
        return ', '.join([day.name for day in obj.available_at.all()])


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('time', 'service')


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'phone',
        'date',
        'time_slot',
        'party_size',
        'remarks',
        'managed_by',
        'created_at',
        'updated_at',
    )
    inlines = [ReservationTableTypeDetailInline]
