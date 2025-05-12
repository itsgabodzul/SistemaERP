from django.shortcuts import render
from apps.cliente.models import m_cliente


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
    return render(request, 'public/inicio.html',{'total_clientes': total_clientes})

def p_vehiculo(request):
    return render(request, 'vehiculos/vehiculos.html')

def p_inventario(request):
    return render(request, 'inventario/inventario.html')

def p_orden(request):
    return render(request, 'ordenes/ordenes.html')

def p_perfil(request):
    return render(request, 'public/perfil.html')

def p_config(request):
    return render(request, 'public/configuracion.html')

def p_help(request):
    return render(request, 'public/help.html')
