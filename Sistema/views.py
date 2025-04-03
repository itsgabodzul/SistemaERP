from django.shortcuts import render
from apps.cliente.models import m_cliente

#Paginas privadas
def v_inicio(request):
    return render(request, 'inicio.html', {})

def v_home(request):
    qClienteTodo = m_cliente.objects.all()
    context = {'clientes':qClienteTodo}
    return render(request, 'public/public_inicio.html', context)