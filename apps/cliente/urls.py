"""
URL configuration for Sistema project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

#Importar las vistas del proyecto
from . import views

#Inclus para que funcione
from django.urls import include

urlpatterns = [
    #Paginas publicas
    path('', views.p_cliente, name='clientes'),
    path('agregar-cliente', views.agregar_cliente, name='agregar_cliente'),
    path('editar-cliente/<int:id_cliente>/', views.editar_cliente, name='editar_cliente'),
    path('ver-cliente/<int:id_cliente>/', views.ver_cliente, name='ver_cliente'),
    path('eliminar-cliente/', views.eliminar_cliente, name='eliminar_cliente'),
    path('agregar-cliente-modal/', views.cliente_modal, name='cliente_modal'),
]