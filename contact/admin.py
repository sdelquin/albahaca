from django.contrib import admin

from .models import Info, Vacation


@admin.register(Info)
class InfoAdmin(admin.ModelAdmin):
    list_display = ('street', 'city', 'state', 'zip_code', 'country', 'email')


@admin.register(Vacation)
class VacationAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'end_date')
