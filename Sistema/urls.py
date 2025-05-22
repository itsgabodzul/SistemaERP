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
    path('admin/', admin.site.urls),

    #Paginas publicas
    path('', views.v_login, name = "u_home"),
    path('inicio/', views.p_inicio, name='inicio'),
    path('clientes/', include('apps.cliente.urls')), #Incluir las url de las apps
    path('vehiculos/', views.p_vehiculo, name='vehiculos'),
    path('inventario/', include('apps.inventario.urls')),
    path('orden/', views.p_orden, name='orden'),
    path('configuracion/perfil/', views.p_perfil, name='perfil'),
    path('configuracion/', views.p_config, name='config'),
    path('configuracion/ayuda/', views.p_help, name='help'),
]