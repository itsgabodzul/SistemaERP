from django.shortcuts import render,  redirect
from apps.cliente.models import m_cliente
from .forms import ClienteForm


def agregar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clientes')
    else:
        form = ClienteForm()

    return render(request, 'clientes/agregar.html',  {'form': form})


def p_cliente(request):
    lista_clientes = m_cliente.objects.all().order_by('-date_created')  # opcionalmente ordenados
    return render(request, 'clientes/clientes.html', {'clientes': lista_clientes})

def editar_cliente(request):
    return render(request, 'clientes/editar.html')

# def p_agregar(request):
#     return render(request, 'clientes/agregar.html')
