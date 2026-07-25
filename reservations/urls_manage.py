from django.urls import path

from . import views_manage as views

app_name = 'reservations-manage'

urlpatterns = [
    path('', views.index, name='index'),
]
