from django.contrib import admin
from django.urls import path

#Importar las vistas del proyecto
from . import views

urlpatterns = [
    #Paginas publicas
    path('', views.p_orden, name='orden'),
    path('generar-nueva-orden', views.crear_orden_trabajo, name='nueva_orden'),
    # path('editar-producto/<int:id_producto>/', views.editar_producto, name='editar_producto'),
    # path('ver-producto/<int:id_producto>/', views.ver_producto, name='ver_producto'),
    # path('eliminar-producto/', views.eliminar_producto, name='eliminar_producto'),
]