from django.shortcuts import redirect
from django.urls import path

from . import views_manage as views

app_name = 'reservations'

urlpatterns = [
    path('', views.index, name='index'),
    path('crear/', lambda r: redirect('reservations:create-phase-date'), name='create'),
    path('crear/fecha/', views.create_phase_date, name='create-date-phase'),
]
