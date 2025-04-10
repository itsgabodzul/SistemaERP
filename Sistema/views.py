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
    return render(request, 'public/inicio.html')