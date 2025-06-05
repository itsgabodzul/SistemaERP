from django.contrib import admin
from django.urls import path
from django.urls import include

#Importar las vistas del proyecto
from . import views

urlpatterns = [
    #Paginas publicas
    path('', views.p_orden, name='orden'),
    path('generar-nueva-orden', views.crear_orden_trabajo, name='nueva_orden'),
    path('editar-orden/<int:id_orden>/', views.editar_orden, name='editar_orden'),
    path('ver-orden/<int:id_orden>/', views.ver_orden, name='ver_orden'),
    # path('eliminar-producto/', views.eliminar_producto, name='eliminar_producto'),
    path('orden/<int:id_orden>/cambiar-estado/<str:nuevo_estado>/', views.cambiar_estado, name='cambiar_estado'),
    path('vehiculos/', include('apps.vehiculo.urls')),
]