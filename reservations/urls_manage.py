from django.urls import path

from . import views_manage as views

app_name = 'reservations'

urlpatterns = [
    path('', views.index, name='index'),
]
