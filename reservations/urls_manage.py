from django.urls import path

from . import views_manage as views

app_name = 'reservations'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:year>/<int:month>/', views.month, name='month'),
    path('<int:year>/<int:month>/<int:day>/', views.services, name='services'),
    path('<int:year>/<int:month>/<int:day>/<str:service_code>/', views.service, name='service'),
    path(
        '<int:year>/<int:month>/<int:day>/<str:service_code>/listar/',
        views.list_service_reservations,
        name='list-service-reservations',
    ),
    path(
        '<int:year>/<int:month>/<int:day>/<str:service_code>/crear/',
        views.create_service_reservation,
        name='create-service-reservation',
    ),
]
