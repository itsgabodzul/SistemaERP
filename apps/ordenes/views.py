from django.shortcuts import render, redirect, get_object_or_404
from .models import m_refaccion, m_orden_trabajo, DetalleServicio
from .forms import OrdenTrabajoForm, RefaccionFormSet, ServicioFormSet
from django.contrib import messages


# Create your views here.
def p_orden(request):
    # query = request.GET.get('busca_cliente')  # Captura lo que escribió el usuario
    ordenes = m_orden_trabajo.objects.all()

    # if query:
    #     clientes = clientes.filter(
    #         Q(nombre__icontains=query) |
    #         Q(ap_01__icontains=query) |
    #         Q(email__icontains=query)
    #     )

    context = {
        'ordenes': ordenes,
        # 'query': query,  # Para mostrar el valor buscado en el input
    }
    return render(request, 'ordenes/ordenes.html', context)

from django.db import transaction

def crear_orden_trabajo(request):
    if request.method == 'POST':
        form = OrdenTrabajoForm(request.POST)
        formset = RefaccionFormSet(request.POST, queryset=m_refaccion.objects.none())
        formset_servicios = ServicioFormSet(request.POST, queryset=DetalleServicio.objects.none(), prefix='servicio')

        if form.is_valid() and formset.is_valid() and formset_servicios.is_valid():
            try:
                with transaction.atomic():  # ¡Todo o nada!
                    # Guarda la orden (estado Pendiente por defecto)
                    orden = form.save(commit=False)
                    orden.estado = 'P'  # 'P' de Pendiente (según tu modelo)
                    orden.save()  # Guarda para obtener PK

                    # Procesa las refacciones
                    refacciones = formset.save(commit=False)
                    for refaccion in refacciones:
                        refaccion.orden = orden
                        refaccion.save()  # Aquí se descuenta del inventario (por el save() de m_refaccion)

                    # Procesa los servicios (¡esto faltaba!)
                    servicios = formset_servicios.save(commit=False)
                    for servicio in servicios:
                        servicio.orden = orden
                        servicio.save()

                    # Actualiza el total de la orden (ahora incluye refacciones)
                    orden.total = orden.calcular_total()
                    orden.save()

                    return redirect('orden')  # Redirige a la lista de órdenes

            except Exception as e:
                # Maneja errores (ej: stock insuficiente)
                form.add_error(None, f"Error al crear la orden: {str(e)}")

    else:
        form = OrdenTrabajoForm()
        formset = RefaccionFormSet(queryset=m_refaccion.objects.none())
        formset_servicios = ServicioFormSet(queryset=DetalleServicio.objects.none(), prefix='servicio')

    return render(request, 'ordenes/nueva_orden.html', {
        'form': form,
        'formset': formset,
        'formset_servicios': formset_servicios,
    })


def ver_orden(request, id_orden):
    orden = get_object_or_404(m_orden_trabajo, pk=id_orden)
    refaccion = m_refaccion.objects.filter(orden=orden)

    if request.method == 'POST' and 'cancelar_orden' in request.POST:
        if orden.estado in ['P', 'E']:  # Solo cancelar si está Pendiente o En Proceso
            orden.estado = 'C'
            orden.save()
            messages.success(request, 'orden|cancelada|Orden cancelada correctamente')
            return redirect('orden')
        else:
            messages.error(request, 'No se puede cancelar una orden terminada')

    context = {
        'orden': orden,
        'refaccion': refaccion,
    }
    return render(request, 'ordenes/ver_orden.html', context)

def cambiar_estado(request, id_orden, nuevo_estado):
    orden = get_object_or_404(m_orden_trabajo, pk=id_orden)
    
    # Validar transiciones permitidas
    transiciones = {
        'P': ['E'],  # Pendiente → En proceso
        'E': ['T'],  # En proceso → Terminado
    }
    
    if orden.estado in transiciones and nuevo_estado in transiciones[orden.estado]:
        orden.estado = nuevo_estado
        orden.save()
        messages.success(request, 'orden|actualizado|'f'Orden {orden.get_estado_display()} correctamente')
    else:
        messages.error(request, 'Transición de estado no permitida')
    
    return redirect('ver_orden', id_orden=id_orden)