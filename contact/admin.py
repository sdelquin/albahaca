from django.contrib import admin

from .models import Info


@admin.register(Info)
class InfoAdmin(admin.ModelAdmin):
    list_display = ('street', 'city', 'state', 'zip_code', 'country', 'email')
