from django.shortcuts import render
from django.contrib import messages
from django.db.models import Q
from apps.cliente.models import m_cliente
from apps.inventario.models import m_inventario
from apps.vehiculo.models import m_vehiculo


#Paginas privadas
def v_inicio(request):
    return render(request, 'inicio.html', {})

#Paginas publicas
def v_login(request):
    qClienteTodo = m_cliente.objects.all()
    context = {'clientes':qClienteTodo}
    return render(request, 'public/login.html', context)

def p_inicio(request):
    total_clientes = m_cliente.objects.count()
    total_vehiculos = m_vehiculo.objects.count()
    productos = m_inventario.objects.all()
    stock_minimo = 5

    productos = productos.filter(stock__lte=stock_minimo)
    total_minimos = productos.filter(stock__lte=stock_minimo).count()

    context ={
        'total_clientes': total_clientes ,
        'total_vehiculos': total_vehiculos ,
        'total_minimos': total_minimos
    }
    return render(request, 'public/inicio.html', context)


def p_perfil(request):
    return render(request, 'public/perfil.html')

def p_config(request):
    return render(request, 'public/configuracion.html')

def p_help(request):
    return render(request, 'public/help.html')
