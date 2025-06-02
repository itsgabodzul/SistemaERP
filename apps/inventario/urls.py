from django.contrib import admin
from django.urls import path

#Importar las vistas del proyecto
from . import views

#Inclus para que funcione
from django.urls import include


urlpatterns = [
    #Paginas publicas
    path('', views.p_productos, name='inventario'),
    path('agregar-producto', views.agregar_producto, name='agregar_producto'),
    path('editar-producto/<int:id_producto>/', views.editar_producto, name='editar_producto'),
    path('ver-producto/<int:id_producto>/', views.ver_producto, name='ver_producto'),
    path('eliminar-producto/', views.eliminar_producto, name='eliminar_producto'),
    path('actualizar-stock/<int:id_producto>/', views.actualizar_stock, name='actualizar_stock'),
    path('vehiculos/cargar_excel/', views.cargar_excel, name='cargar_excel'),
]