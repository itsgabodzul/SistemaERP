from django.shortcuts import render,  redirect, get_object_or_404
from apps.cliente.models import m_cliente
from .forms import ClienteForm
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import Q

def agregar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'cliente|agregado|Cliente agregado correctamente')
            return redirect('clientes')
    else:
        form = ClienteForm()

    return render(request, 'clientes/agregar.html',  {'form': form})


def p_cliente(request):
    clientes = m_cliente.objects.all().order_by('-date_created')
    query = request.GET.get('busca_cliente')  # Captura lo que escribió el usuario
    clientes = m_cliente.objects.all()

    if query:
        clientes = clientes.filter(
            Q(nombre__icontains=query) |
            Q(ap_01__icontains=query) |
            Q(email__icontains=query)
        )

    context = {
        'clientes': clientes,
        'query': query,  # Opcional: para mostrar el valor buscado en el input
    }
    return render(request, 'clientes/clientes.html', {'clientes': clientes})

def editar_cliente(request, id_cliente):
    cliente = get_object_or_404(m_cliente, pk=id_cliente)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'cliente|actualizado|Cliente actualizado correctamente')
            # return redirect('clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'clientes/editar.html', {'form': form, 'cliente': cliente})

def ver_cliente(request, id_cliente):
    cliente = get_object_or_404(m_cliente, pk=id_cliente)
    return render(request, 'clientes/ver_cliente.html', {'cliente': cliente})

@require_POST
def eliminar_cliente(request):
    id_cliente = request.POST.get('id_cliente')
    cliente = get_object_or_404(m_cliente, pk=id_cliente)
    cliente.delete()
    messages.success(request, f"'{cliente.nombre}' eliminado correctamente.")
    return redirect('clientes')


# def busca_cliente(request):
#     query = request.GET.get('busca_cliente')  # Captura lo que escribió el usuario
#     clientes = m_cliente.objects.all()

#     if query:
#         clientes = clientes.filter(
#             busca_cliente(nombre__icontains=query) |
#             busca_cliente(ap_01__icontains=query) |
#             busca_cliente(email__icontains=query)
#         )

#     context = {
#         'clientes': clientes,
#         'query': query,  # Opcional: para mostrar el valor buscado en el input
#     }
#     return render(request, 'clientes/clientes.html', context)
# # def p_agregar(request):
#     return render(request, 'clientes/agregar.html')
