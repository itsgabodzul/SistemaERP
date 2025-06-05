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
from apps.vehiculo.views import ClienteAutocomplete
from apps.ordenes.views import VehiculoAutocomplete


urlpatterns = [
    path('admin/', admin.site.urls),

    #Paginas publicas
    path('login/', views.login_view, name = "u_home"),
    path('', views.logout_view, name = "logout"),
    path('inicio/', views.p_inicio, name='inicio'),
    path('clientes/', include('apps.cliente.urls')), #Incluir las url de las apps
    path('vehiculos/',include('apps.vehiculo.urls')),
    path('inventario/', include('apps.inventario.urls')),
    path('orden-de-trabajo/', include('apps.ordenes.urls')),
    path('configuracion/perfil/', views.p_perfil, name='perfil'),
    path('configuracion/', views.p_config, name='config'),
    path('cliente-autocomplete/', ClienteAutocomplete.as_view(), name='cliente-autocomplete'),
    path('vehiculo-autocomplete/', VehiculoAutocomplete.as_view(), name='vehiculo-autocomplete'),
    path('configuracion/eliminar-categoria', views.eliminar_categoria, name='eliminar_categoria'),
    path('configuracion/eliminar-servicio', views.eliminar_servicio, name='eliminar_servicio'),
    path('configuracion/editar-servicio', views.editar_servicio, name='editar_servicio'),
    path('configuracion/eliminar-empleado', views.eliminar_empleado, name='eliminar_empleado'),
    path('configuracion/editar-empleado', views.editar_empleado, name='editar_empleado'),
    # path('select2/', include('django_select2.urls')),
]