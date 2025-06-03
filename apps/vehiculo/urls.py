from django.contrib import admin
from django.urls import path, include

#Importar las vistas del proyecto
from . import views

#Inclus para que funcione
from django.urls import include


urlpatterns = [
    #Paginas publicas
    path('', views.p_vehiculo, name='vehiculos'),
    path('agregar-vehiculo', views.agregar_vehiculo, name='agregar_vehiculo'),
    path('editar-vehiculo/<int:id_vehiculo>/', views.editar_vehiculo, name='editar_vehiculo'),
    path('ver-vehiculo/<int:id_vehiculo>/', views.ver_vehiculo, name='ver_vehiculo'),
    path('eliminar-vehiculo/', views.eliminar_vehiculo, name='eliminar_vehiculo'),
    path('api/marcas/', views.obtener_marcas, name='api_marcas'),
    path('api/modelos/<str:marca>/', views.obtener_modelos, name='api_modelos'),
    path('clientes/', include('apps.cliente.urls')),
]