from django.urls import path

from . import views_manage as views

app_name = 'reservations'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:year>/<int:month>/', views.month, name='month'),
    path('<int:year>/<int:month>/<int:day>/', views.day, name='day'),
    path('<int:year>/<int:month>/<int:day>/<str:service_code>/', views.service, name='service'),
]
