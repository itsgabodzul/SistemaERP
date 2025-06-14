from django.shortcuts import render,  redirect, get_object_or_404
from apps.cliente.models import m_cliente
from apps.vehiculo.models import m_vehiculo
from .forms import ClienteForm
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

#Definir las vistas de cada pagina

#Página de clientes (index)
@login_required
def p_cliente(request):
    query = request.GET.get('busca_cliente')  # Captura lo que escribió el usuario
    clientes = m_cliente.objects.all().order_by('-date_created')

    if query:
        clientes = clientes.filter(
            Q(nombre__icontains=query) |
            Q(ap_01__icontains=query) |
            Q(email__icontains=query) |
            Q(telefono__icontains=query)
        )

    context = {
        'clientes': clientes,
        'query': query,  # Para mostrar el valor buscado en el input
    }
    return render(request, 'clientes/clientes.html', context)

#Página de Agregar Cliente
@login_required
def agregar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST) #Para guardar un formulario
        if form.is_valid():
            form.save()
            messages.success(request, 'cliente|agregado|Cliente agregado correctamente')
            return redirect('clientes') #Redireccionamiento
    else:
        form = ClienteForm()

    return render(request, 'clientes/agregar.html',  {'form': form}) #Renderizar la página desde la plantila

#Página de Editar Cliente
@login_required
def editar_cliente(request, id_cliente):
    cliente = get_object_or_404(m_cliente, pk=id_cliente)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'cliente|actualizado|Cliente actualizado correctamente')
            return redirect('clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'clientes/editar.html', {'form': form, 'cliente': cliente})

#Página de Ver Cliente
@login_required
def ver_cliente(request, id_cliente):
    cliente = get_object_or_404(m_cliente, pk=id_cliente) #Para pasar la id

    context = {
        'cliente': cliente,
    }
    return render(request, 'clientes/ver_cliente.html', context)


#Eliminar Cliente  (Con Post para mayor seguridad)
@require_POST
def eliminar_cliente(request):
    id_cliente = request.POST.get('id_cliente')
    cliente = get_object_or_404(m_cliente, pk=id_cliente)
    cliente.delete()
    messages.success(request, 'cliente|eliminado|Cliente eliminado correctamente')
    return redirect('clientes')

def cliente_modal(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, })
        return render(request, 'clientes/cliente_modal_form.html', {'form': form})
    else:
        form = ClienteForm()
        return render(request, 'clientes/cliente_modal_form.html', {'form': form})


def ver_vehiculo_asociado(request, id_vehiculo):
    vehiculo = get_object_or_404(m_vehiculo, pk=id_vehiculo) #Para pasar la id
    return render(request, 'vehiculos/ver_vehiculo.html', {'vehiculo': vehiculo})