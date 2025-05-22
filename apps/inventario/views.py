from django.shortcuts import render, redirect, get_object_or_404
from .forms import InventarioForm
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import Q
from apps.inventario.models import m_inventario

# Create your views here.
from django.db.models import Q

def p_productos(request):
    # Valores iniciales
    stock_minimo = 5  # Puedes hacer esto configurable como vimos antes
    productos = m_inventario.objects.all()
    # Filtros
    query = request.GET.get('query')  # Para búsqueda general
    query2 = request.GET.get('busca_producto')  # Para búsqueda específica
    solo_minimos = request.GET.get('solo_minimos') == '1'
    # Aplicar filtros en el orden correcto
    if query:
        productos = productos.filter(
            Q(nombre_p__icontains=query) |
            Q(descripcion__icontains=query) |
            Q(categoria__categoria__icontains=query)
        )
    if query2:
        productos = productos.filter(
            Q(nombre_p__icontains=query2)  # Cambiado a nombre_p para coincidir con tu modelo
        )
    if solo_minimos:
        productos = productos.filter(stock__lte=stock_minimo)
    # Contador de productos en mínimo
    total_minimos = productos.filter(stock__lte=stock_minimo).count()

    context = {
        'productos': productos,
        'stock_minimo': stock_minimo,
        'query': query or query2,  # Para mostrar en el input de búsqueda
        'total_minimos': total_minimos,
        'solo_minimos': solo_minimos,
    }
    return render(request, 'inventario/inventario.html', context)


def agregar_producto(request):
    if request.method == 'POST':
        form = InventarioForm(request.POST) #Para guardar un formulario
        if form.is_valid():
            form.save()
            messages.success(request, 'producto|agregado|Producto agregado correctamente')
            return redirect('inventario') #Redireccionamiento
    else:
        form = InventarioForm()

    return render(request, 'inventario/agregar_producto.html',  {'form': form})

def ver_producto(request, id_producto):
    producto = get_object_or_404(m_inventario, pk=id_producto) #Para pasar la id
    return render(request, 'inventario/ver_producto.html', {'producto': producto})

def editar_producto(request, id_producto):
    producto = get_object_or_404(m_inventario, pk=id_producto)
    if request.method == 'POST':
        form = InventarioForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'prodcuto|actualizado|Prodcuto actualizado correctamente')
            return redirect('inventario')
    else:
        form = InventarioForm(instance=producto)
    return render(request, 'inventario/editar_producto.html', {'form': form, 'producto': producto})

@require_POST
def eliminar_producto(request):
    id_producto = request.POST.get('id_producto')
    producto = get_object_or_404(m_inventario, pk=id_producto)
    producto.delete()
    messages.success(request, 'producto|eliminado|Producto eliminado correctamente')
    return redirect('inventario')

def actualizar_stock(request, id_producto):
    producto = get_object_or_404(m_inventario, pk=id_producto)
    stock_anterior = producto.stock

    if request.method == 'POST':
        try:
            cantidad_agregada = int(request.POST.get('stock'))
            if cantidad_agregada < 0:
                raise ValueError("El stock no puede ser negativo")
            producto.stock += cantidad_agregada
            producto.save()
            messages.success(request, 'prodcuto|actualizado|Stock actualizado correctamente')
            return redirect('inventario')
        except ValueError as e:
            messages.error(request, f'Error: {str(e)}')

    return render(request, 'inventario/actualizar_stock.html', {'producto': producto})