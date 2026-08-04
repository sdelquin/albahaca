from django.urls import path

from . import views_manage as views

app_name = 'reservations'

urlpatterns = [
    path('', views.index, name='index'),
    path('mes/<int:year>/<int:month>/', views.month, name='month'),
    path('mes/', views.month, name='month'),
]
