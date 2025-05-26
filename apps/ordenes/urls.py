from django.contrib import admin
from django.urls import path

#Importar las vistas del proyecto
from . import views

urlpatterns = [
    #Paginas publicas
    path('', views.p_orden, name='orden'),
    path('generar-nueva-orden', views.crear_orden_trabajo, name='nueva_orden'),
    # path('editar-producto/<int:id_producto>/', views.editar_producto, name='editar_producto'),
    path('ver-orden/<int:id_orden>/', views.ver_orden, name='ver_orden'),
    # path('eliminar-producto/', views.eliminar_producto, name='eliminar_producto'),
    path('orden/<int:id_orden>/cambiar-estado/<str:nuevo_estado>/', views.cambiar_estado, name='cambiar_estado'),
]